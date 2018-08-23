# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 16:24:45 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)

"""
#pylint: disable=C0326

import random
import math
from collections import OrderedDict
from typing import List, Callable, Dict
from inst_func_eval import InstFunEvaluator


def coordinate_descent( fun : Callable[ [List[float]], float ],
                        param_grid_dic : Dict[str, List[float]],
                        x_idxs : List[int],
                        eval_budget : int = 1000,
                        seed : int =1337,
                        log_level=0) :

    assert isinstance( param_grid_dic, OrderedDict), "param_grid_dic should be an OrderedDict"

    fun_eval = InstFunEvaluator( fun, param_grid_dic)

    max_idxs = [ len( rng ) - 1  for rng in param_grid_dic.values() ]

    if x_idxs is None :
            x_idxs = [ random.randrange(0, max_idx) for max_idx in max_idxs]

    best_val = float( "inf" )
    best_idxs = []

    while fun_eval.eval_cnt() < eval_budget :
        fun_val, x_idxs = coordinate_descent0( fun_eval, x_idxs, max_idxs )
        if fun_val < best_val :
            best_val = fun_val
            best_idxs = x_idxs

        x_idxs = [ random.randrange(0, max_idx) for max_idx in max_idxs ]

    return best_val, best_idxs, fun_eval


def coordinate_descent0( fun_eval : Callable[ [List[float]], float ],
                        #param_grid_dic : Dict[str, List[float]],
                        x_idxs : List[int],
                        max_idxs,
                        eval_budget : int = 1000,
                        seed : int =1337,
                        log_level=0) :

    """ Implements coordinate descent method for a function of n parameters
    param_grid should be a list of n lists, with the d-th list specifying
    a list of possible values for the d-th parameter
    """

    random.seed( seed )

    fun_val = fun_eval.from_idxs( x_idxs )

    ite = 0
    while fun_eval.eval_cnt() < eval_budget :
        #    print( "\n\n** iter=%d start fun_next=%.4f x_idxs=%s" % (ite, fun_val, x_idxs) )
        fun_next, x_idxs_next = take_one_step( fun_eval, fun_val,
                                               eval_budget, x_idxs, max_idxs )
        ite += 1
        if log_level > 0 :
            print( "** iter=%d - end fun_next=%.4f x_idxs=%s" % (ite, fun_val, x_idxs) )

        if fun_next >= fun_val :
            # got stuck
            return fun_val, x_idxs

        fun_val = fun_next
        x_idxs  = x_idxs_next

    return fun_val, x_idxs


def take_one_step( fun_eval : InstFunEvaluator, fun_val : float, eval_budget : int,
                   x_idxs  : List[int], max_idxs : List[int] ) :
    """Generate a new function evaluation position and the corresponding
    value that is less than or equal the current fun_val"""

    n_params = len( x_idxs )

    min_dirs = [ ]
    # Try each direction in turn
    for di in range(n_params) :
        min_di = minimize_along_d( fun_eval, fun_val, di, x_idxs, max_idxs[di] )
        min_dirs.append( min_di )
        if fun_eval.eval_cnt() > eval_budget :
            break

    #print( mins_dirs )
    return min( min_dirs, key = lambda pair : pair[0]  )


def minimize_along_d( fun_eval, fun_val, d : int,  x_idxs_ : List[int],
                      max_idx_d : List[int], log_level : int=0) :
    """ Search for a local mininim by moving along direction d  """
    #first identify descent direction
    #xp_idxs = x_idxs.copy()

    fun_val_r = float( "nan" )
    fun_val_l = float( "nan" )
    fun_next  = float( "nan" )
    x_idxs = x_idxs_.copy()

    if x_idxs[d] < max_idx_d  :
        x_idxs_r = x_idxs.copy()
        x_idxs_r[d] += 1
        fun_val_r = fun_eval.from_idxs( x_idxs_r )

    if x_idxs[d] > 0 :
        x_idxs_l = x_idxs.copy()
        x_idxs_l[d] -= 1
        fun_val_l = fun_eval.from_idxs( x_idxs_l )

    step = 0

    if log_level > 0 :
        print( "\nMinimizing along d=%d x_idxs=%s fun_val=%.4f fun_val_l=%.4f fun_val=%.4f" %
              (d, x_idxs, fun_val_r, fun_val_l, fun_val) )

    if   ( (fun_val_r < fun_val_l) or math.isnan(fun_val_l)) and  fun_val_r < fun_val :
        # right is steepest descent direction
        step = +1
        fun_next = fun_val_r
        x_idxs = x_idxs_r

    elif ( (fun_val_l <= fun_val_r) or math.isnan(fun_val_r) ) and fun_val_l <= fun_val :
        step = -1
        fun_next = fun_val_l
        x_idxs = x_idxs_l

    elif (( fun_val <= fun_val_r or math.isnan(fun_val_r) ) and
           (fun_val <  fun_val_l or math.isnan(fun_val_l) )     )  :
        # we are already at local minimum along direction d
        return fun_val, x_idxs

    else :
        assert False, ( f"This shouldn't happen: d={d},  fun_val={fun_val} "
                        f"fun_val_r={fun_val_r}, fun_val_l={fun_val_l}" )

    if log_level > 1 :
        print( "d=%d step=%d fun_next=%.4f" % (d, step, fun_next) )

    if step == 0 :
        # we are already at local minimum along direction d
        return fun_val, x_idxs

    fun_old : float = fun_val

    while True :

        if (x_idxs[d] + step) > max_idx_d  or (x_idxs[d]+step) < 0 :
            return fun_next, x_idxs

        fun_old  = fun_next
        x_idxs_old = x_idxs.copy()

        x_idxs[d] += step
        fun_next = fun_eval.from_idxs( x_idxs )
        if log_level > 1 :
            print( "after fun_eval: x_idxs=%s f=%.6f" % (x_idxs, fun_next) )

        if not (fun_next < fun_old) :
            if log_level > 1 :
                print( "No longer decreasing fun_next(%s)= %.6f  fun_old(%s)=%.6f"
                      % (x_idxs, fun_next, x_idxs_old, fun_old))
            return fun_old, x_idxs_old
        if log_level > 1 :
            print( "xp_idxs=%s fun_next=%.3f" % (x_idxs, fun_next) )

    return fun_next, x_idxs


def test0() :
    import numpy as np

    def banana( x : List[float] ) -> float :
        """f(x,y)=(a-x)^{2}+b(y-x^{2})^{2}"""
        return (1 - x[0])**2 + 100 * (x[1] -x[0]**2) ** 2

    param_grid = [ np.arange( -2, 2, 0.01 ),
                   np.arange( -2, 2, 0.01 ) ]

    x_idxs = [61, 395 ]

    fun_eval = InstFunEvaluator( banana, param_grid, log=True )
    #%%
    fun_eval( [61,394] )
    #%%
    fun_eval( [298,295] )
    #%%
    #coordinate_descent( fun_eval, param_grid, x_idxs )
    #%%
    x_idxs = [298, 297]
    coordinate_descent( banana, param_grid, x_idxs )
    #%%

def test1( param_grid_dic, train_xgb ) :
    param_names = list( param_grid_dic.keys())
    fun = lambda param_vals : -train_xgb( data, dict( zip(param_names, param_vals)), memoization_path  )

    #x_idxs=[5, 4, 2, 3, 2]
    #x_idxs=[2, 0, 2, 3, 0]
    x_idxs= [0, 0, 0, 1, 0]

    ret = coordinate_descent( fun, param_grid, x_idxs )
    #%%


def test2( param_grid_dic, train_xgb ) :
    #%%
    param_names = list( param_grid_dic.keys())
    fun = lambda param_vals : -train_xgb( data, dict( zip(param_names, param_vals)), memoization_path  )


    max_idxs = [ len( param_vals ) - 1  for param_vals in param_grid  ]


    x_idxs= [0, 0, 0, 1, 0]

    #&%%
    nb = neighborhood(x_idxs, max_idxs)
    #%%

    fun_eval = InstFunEvaluator( fun, param_grid, log=True )
    #%%
    results = [ (fun_eval(x_idxs), x_idxs) ] + [ (fun_eval( tup ), tup) for tup in nb ]

    sorted( results, key= lambda x : x[0] )
    #%%
def neighborhood( x_idxs, max_idxs ) :

    n_dirs = len(x_idxs)

    def inc( x_idxs, d, delta ) :
        ret = x_idxs.copy()
        ret[d] += delta
        return ret

    def is_within_bounds( x_idxs, max_idxs ) :
        return all( (x_idxs[d] >= 0 and x_idxs[d] <= max_idxs[d]) for d in range(len(x_idxs))  )

    ups  = [ inc(x_idxs, d, +1) for d in range(len(x_idxs)) ]
    downs = [ inc(x_idxs, d, -1) for d in range(len(x_idxs)) ]

    return [ tup for tup in ups + downs if is_within_bounds( tup, max_idxs ) ]
#%%

#    ret = coordinate_descent( fun, param_grid, x_idxs )


#def test1(data, train_xgb) :
    #%%
    #%%

if __name__ == "__main__" :
    pass
    #%%
