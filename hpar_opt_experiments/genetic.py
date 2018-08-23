# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 09:37:38 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""

import random

from collections import namedtuple
from functools import  total_ordering
import queue as Q
import bisect


#%%

@total_ordering
class EvaluatedIndiv :

    def __init__(self, indiv, fitness, gen_num) :
        self.indiv = indiv
        self.fitness = fitness
        self.gen_num = gen_num

    def __eq__( self, other ) :
        return (self.indiv == other.indiv) and (self.fitness == other.fitness)

    def __ne__( self, other ) :
        return not self.eq( other )

    def __lt__( self, other ) :
        return self.fitness > other.fitness

    def __str__(self ) :
        return ( "EvaluatedIndiv( indiv=%s, fitness=%.6g, gen_num=%d)" %
                 (self.indiv, self.fitness, self.gen_num) )

    def __repr__(self) :
        return str(self)
#%%

def genetic_algorithm(  fitness_fun, gene_names, genes_grid, init_pop = None,
                        pop_size = 10, n_gen=100, mutation_prob=0.1, normalize=None, seed=1337 ) :
    """
    Implementation of genetic algorithms logic tailored for hyper-parameter optimization:

    Section 4.2, Rusell & Norvig,   Artificial Intelligence a modern a approach, Prentice Hall, 3rd Edition
    http://aima.cs.berkeley.edu/

    A reference implementation where individuals are encoded as sequences is given here:
        https://github.com/aimacode/aima-python/blob/master/search.py
    See function genetic_algorithm and related ones.

    In our implementation, an **individual** is just a dictionary mapping parameter names to values,
    ej.   {  "num_trees" : 100,  "max_tree_depth": 5,  "min_leaf_split" : 5, ... }

    A fitness function is one that takes such a dictionary as a single argument
    and returns a fitness score. The objective is to _maximize_ the fitness function.

    Genetic algoritms assume these parameters have an order that makes sense for the cross-over
    operation. For a discussion on why this matters see page 128 of refence above.
    This order is specified through the param_names argument


    Parameters:

    init_pop: an initial list of individuals

    gene_names : a list of strings specifying the parameters for fitness
                 function in an order that makes sense for doing genetic
                 recombination (see comment above and recombine function)

    fitness_fun : a real-valued function that takes a dictionary as a parameter

    mutation_prob : probability of mutating an individual

    genes_grid : dictionary with entries ('param_value' : [ list of possible values for param ] )

    n_gen : number of generations

    Returns:

    """

    random.seed( seed  )
    num_evaluations=0

    if init_pop is None :
        init_pop = init_population(pop_size, gene_names, genes_grid)

    pop_size = len(init_pop)

    evaluated_pop = [ EvaluatedIndiv(indiv=indiv, fitness=fitness_fun(indiv),
                                     gen_num=0)
                      for indiv in init_pop ]

    all_indivs = evaluated_pop.copy()

    num_evaluations += pop_size

    for gen_num in range(1, n_gen + 1 ) :
        evaluated_pop = run_one_generation( evaluated_pop, fitness_fun, gene_names,
                                            genes_grid, mutation_prob, normalize, gen_num  )
        all_indivs.extend( evaluated_pop )
        num_evaluations += pop_size

        print( "gen: %d best_indiv: %s, best_ever:%s" %
               (gen_num, max(evaluated_pop, key=lambda i : i.fitness),
                max( all_indivs, key = lambda i : i.fitness ) ) )

    return sorted( all_indivs, key= lambda ei : ei.fitness, reverse=True )


def init_population(pop_size, gene_names, genes_grid):
    """Initializes population for genetic algorithm
    pop_size    :  Number of individuals in population
    gene_pool   :  List of possible values for individuals
    state_length:  The length of each individual"""

    #n_genes = len(gene_names)

    def make_one( ) :
        return { name : genes_grid[name][random.randrange(0, len(genes_grid[name]))]
                 for name in gene_names  }

    population = [ make_one() for i in range(pop_size) ]

    return population

def run_one_generation( evaluated_pop, fitness_fun, gene_names,
                        genes_grid, mutation_prob, normalize, gen_num ) :

    pop_size = len( evaluated_pop )

    new_evaluated_pop = []  # new population

    for i in range( pop_size  ) :

        fitnesses = [ evind.fitness  for evind in evaluated_pop ]

        if normalize is not None :
            fitnesses1 = normalize( fitnesses )
        else :
            fitnesses1 = fitnesses

        sampler = weighted_sampler(evaluated_pop, fitnesses1)

        father = sampler( )
        mother = sampler( )

        child0 = recombine( mother.indiv, father.indiv, gene_names )
        mutated = mutate( child0, genes_grid, mutation_prob, gene_names )

        ev_indiv = EvaluatedIndiv(indiv=mutated,
                                  fitness=fitness_fun(mutated),
                                  gen_num=gen_num )

        new_evaluated_pop.append( ev_indiv )

    return new_evaluated_pop

#%%

def recombine( mother, father, gene_names ) :
    """Simulate sexual recombination of two dna's"""
    n_genes = len(mother)
    cut = random.randrange( 0, n_genes )

    # take first cut values from mother's genes
    # last n -gebnes  values from father's genes
    # using generators because we are cool.

    child = {  name : mother[name] for name in gene_names[:cut] }
    child.update( (name , father[name])  for name in gene_names[cut:] )

    return child

def mutate( indiv, genes_grid, mutation_prob, gene_names):

    if random.uniform(0, 1) >= mutation_prob:
        return indiv

    mutated_indiv = indiv.copy()
    n_genes = len(indiv)
    gene = gene_names[ random.randrange(0, n_genes) ]

    n_aleles = len(genes_grid[gene])
    ale_idx = random.randrange(0, n_aleles)

    mutated_indiv[gene] = genes_grid[gene][ale_idx]

    return  mutated_indiv


def weighted_sampler(seq, weights):
    """Return a random-sample function that picks from seq weighted by weights.
    Taken directly from: https://github.com/aimacode/aima-python/blob/master/utils.py"""
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)

    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]


def normalizer( gamma, b ) :

    def normalize( fitnesses ) :

        min_f = min( fitnesses )
        max_f = max( fitnesses )
        denom = max_f - min_f

        return [  (f - min_f)/(denom +1e-6) ** gamma + b for f in fitnesses ]

    return normalize


def test( pqueue ) :
    #%%
    genes_grid = {
            "a" : [ 1, 2, 3, 5, 50, 500, 600, 1000],
            "b" : [ 2, -1, 0, 1, 2],
            "c" : [ 2, 3, 4, 5 ],
            "d" : [ 4, 5, 123, 235 ]
            }
    fitness_fun = lambda dic : dic["a"] + dic["b"] + dic["c"] + dic["d"]

    gene_names = ["a", "b", "c", "d"]

    genetic_algorithm(  fitness_fun, gene_names, genes_grid, init_pop = None,
                        pop_size=20, n_gen=100, mutation_prob=0.1, seed=1337 )

    #%%