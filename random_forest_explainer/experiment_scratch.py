# -*- coding: utf-8 -*-
"""
Created on Fri May  4 14:29:45 2018

@author: mrestrepo
"""

def rfc_innards( train_df, rfc ): 
    #%%
    rfc.estimators_  # list of DecisionTreeClassifier 
    
    est= rfc.estimators_[0]
            
    est.tree_ # sklearn.tree._tree.Tree
    #%%
    est.tree_.node_count # number of nodes 
    est.tree_.children_left   # array of int size n-nodes
    est.tree_.children_right  # array of int size n-nodes
    #%%
    est.tree_.weighted_n_node_samples # array of int size 
    #%%
    est.tree.value # ( n_nodes x )
    #%%
    dp = est.tree_.decision_path( train_df.values )    
    #%%    
    # tree = est.tree_
    #%%
    return dp 