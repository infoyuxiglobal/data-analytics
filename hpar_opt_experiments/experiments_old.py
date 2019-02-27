# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 08:47:10 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""
from collections import OrderedDict
from itertools import product
import random

import os
from importlib import reload

import pandas as pd
import xgboost as xgb
#%%
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier
#%%
from memoize import Memoizer
from inst_func_eval import InstFunEvaluator
#%%

# Data preprocessed by:
# data-analytics/tree_classif_explain/mapi_presentation/HC_Default_Risk.ipynb

DATA_DIR = r"C:\_DATA\experimentation\HC_Default_Risk/"

#%%

#%%
def main() :
    #%%
    data0 = { "x_train" : pd.read_pickle( DATA_DIR + "/x_train.pkl" ),
             "y_train" : pd.read_pickle( DATA_DIR + "/y_train.pkl" ),
             "x_test"  : pd.read_pickle( DATA_DIR + "/x_test.pkl" ),
             "y_test"  : pd.read_pickle( DATA_DIR + "/y_test.pkl" ) }

    #%%
    param_grid_dic = OrderedDict([
            ("learning_rate", [0.05, 0.10, 0.15, 0.20, 0.25, 0.30 ] ),
            ("max_depth"    , [  3 , 4 , 5, 6,  8, 10, 12, 15 ] ),
            ("min_child_weight", [ 1, 3, 5, 7 ] ),
            ("gamma", [0.0, 0.1, 0.2, 0.3, 0.4 ]),
            ("colsample_bytree", [  0.3, 0.4, 0.5, 0.7 ] ),
            ])

    #%%
    train_fraction = 0.05
    test_fraction = 0.16
    data = subsample( data0, train_fraction, test_fraction )
    #%%
    memoization_path = DATA_DIR + "/" + "xgboost_memo%g" % train_fraction
    print( "memoization_path= " + memoization_path)
    if not os.path.exists( memoization_path ) :
        os.mkdir( memoization_path )
    #%%
    fun = Memoizer( lambda param_dic : train_xgb( data, param_dic ),
                    memoization_path )
    #%%
    grid_search( param_grid_dic, fun )
    #%%

def grid_search( param_grid_dic, fun, seed, log_level=0 ) :
    #%%
    import inst_func_eval as ife

    param_combos_shuffled = make_param_combos( param_grid_dic, seed=seed)

    best_auc = 0
    #best_combo = None

    fun_eval = ife.InstFunEvaluator( fun, param_grid_dic )

    for i, param_dic  in enumerate( param_combos_shuffled ) :
        auc = fun_eval.eval_fun( param_dic )
        if log_level > 0 :
            print( tuple( param_dic.items() )  )
            print( auc,  " best_auc: ", best_auc  )
        if auc > best_auc :
            best_auc = auc
            #best_combo = param_dic

    #%%
    return fun_eval


def coordinate_descent( param_grid_dic, fun, seed=1359 ) :
    #%%
    import coordescent as cd
    reload(cd)

    #param_grid = param_grid_dic.values()

    fun_min = lambda param_dic : -fun(param_dic)

    random.seed( seed  )

    _, _, fun_eval = cd.coordinate_descent( fun_min, param_grid_dic, x_idxs=None)
    #%%
    return fun_eval
    #%%
def genetic( param_grid_dic, fun ) :
    #%%
    from importlib import reload
    import genetic as g
    reload( g )

    gene_names = list( param_grid_dic.keys())
    genes_grid = param_grid_dic

    gene_result = g.genetic_algorithm( fun,  genes_grid,
                                       init_pop = None, pop_size = 30, n_gen=10,
                                       mutation_prob=0.1,
                                       normalize = g.normalizer( 2.0, 0.01),
                                       seed=1336 )


    #%% 0.7407
    gene_result = g.genetic_algorithm( fun, gene_names, genes_grid,
                                     init_pop = None, pop_size = 30, n_gen=10,
                                     mutation_prob=0.2,
                                     #normalize = g.normalizer( 1.0, 0.3),
                                     seed=1337 )
    #%%
    return gene_result

def test( data, memoization_path ) :
    #%%
    param_dic = OrderedDict([('learning_rate', 0.2),
             ('max_depth', 5),
             ('min_child_weight', 1),
             ('gamma', 0.4),
             ('colsample_bytree', 0.7)])


    train_xgb( data, param_dic, memoization_path=None, model_type='xgb')

    #%%

def subsample( data0, train_fraction, test_fraction, seed=1337 ) :
    data = data0.copy()
    n_train = len(data0["x_train"])
    assert n_train== len(data0["y_train"])
    #%%
    np.random.seed( seed )
    r = np.random.rand(n_train) < train_fraction
    data["x_train"] = data0["x_train"].loc[r]
    data["y_train"] = data0["y_train"].loc[r]

    #%%
    np.random.seed( seed )
    n_test= len( data0["x_test"])
    assert n_test == len(data0["y_test"])

    r = np.random.rand(n_test) < test_fraction

    data["x_test"] = data0["x_test"].loc[r]
    data["y_test"] = data0["y_test"].loc[r]
    #%%
    return data


def make_param_combos( param_grid_dic, seed=1337 ) :
    #param_lens = [ len(v) for v  in param_grid_dic.values() ]
    param_names = list( param_grid_dic.keys() )

    param_idx_ranges = [ range(len(v)) for v in param_grid_dic.values() ]
    all_param_idx_combos = product( *param_idx_ranges  )
    all_param_combos = [  OrderedDict( ( name, param_grid_dic[name][idx])
                                for name, idx in  zip(param_names,idx_combo ) )
                          for idx_combo in all_param_idx_combos   ]
    #%%
    np.random.seed( seed )
    param_combos_shuffled = all_param_combos.copy()
    np.random.shuffle( param_combos_shuffled )
    #%%
    return param_combos_shuffled

#%%

def train_xgb( data, param_dic, model_type='xgb' ) :
    # fit model no training data

    if model_type == 'xgb' :
        model = xgb.XGBClassifier( learning_rate=param_dic["learning_rate"],
                                   max_depth=param_dic["max_depth"],
                                   min_child_weight=param_dic["min_child_weight"],
                                   colsample_bytree=param_dic["colsample_bytree"],
                                   gamma=param_dic["gamma"])
    else :
        model = RandomForestClassifier( n_estimators=100, min_samples_split=50, min_samples_leaf=10, max_depth=12)
    print( type(model) )
    model.fit(data["x_train"], data["y_train"] )

    y_pred = model.predict_proba( data["x_test"] )[:,1]
    auc = roc_auc_score( data["y_test"], y_pred )
    #
    return auc
#%%

def prepare_data( ) :
    #%%
    import sys
    from sklearn.model_selection import train_test_split
    #%%
    sys.path.append( '../utils')
    #%%
    app_fn = DATA_DIR + "application_train.csv"

    df0 = pd.read_csv( app_fn )
    #columns to lowercase
    df0.columns = [ col.lower() for col in df0.columns ]
    #desc = df0.describe().transpose()
    df0 = df0.set_index( 'sk_id_curr')

    df0.rename( columns={ "days_birth" : "age",
                      "name_education_type" : "education",
                      "name_housing_type" : "housing",
                     "name_income_type"  : "income",
                     "name_family_status" : "fam_status",
                     "code_gender" : "gender"}, inplace=True)

    df0['education'] = ( df0['education'].replace('Secondary / secondary special', 'Secondary')
                                     .replace( 'Higher education', 'Higher') )

    #%%

    df1 = df0.copy()
    del df1['organization_type'] # dropped because of too many values
    #del df1['ext_source_1']
    #del df1['ext_source_2']
    #del df1['ext_source_3']
    del df1['occupation_type']
    df1['flag_own_car'] = df0['flag_own_car'] == 'Y'
    df1['flag_own_realty'] = df0['flag_own_realty'] == 'Y'
    cat_vars_0  = df1.dtypes[ df1.dtypes == 'object' ]
    cat_vars_0
    #%%
    import  df_one_hot_encode

    oh_enc = df_one_hot_encode.DfOneHotEncoder( cat_vars_0.index )

    oh_enc.fit( df1 )
    df1 = oh_enc.transform( df1, drop_old=True )
    #%%
    # Convert flag columns to bool
    for col in df1.columns :
        if col.startswith( 'flag_' ) or col.startswith( 'reg_') :
            df1[col] = (df1[col] == 1)

    # For float64 columns impute  NaNs with median
    for col in df1.select_dtypes('float64').columns :
        if df1[col].isnull().sum() > 0 :
            median = df1[col].median()
            df1[col] = df1[col].fillna(  median )
    #%%
    del df0
    #%%
    train, test = train_test_split( df1, train_size = 0.8, test_size = 0.2 )
    Y_train = train['target']
    Y_test  = test['target']

    X_train = train.loc[ : , train.columns != 'target']
    X_test  = test .loc[ : , test.columns != 'target']
    #%%
    del df1, train, test
    #%%
    for (obj, fname) in [ (Y_train, "y_train"), (Y_test, "y_test"),
                      (X_train, "x_train"), (X_test, "x_test") ] :
        obj.to_pickle( DATA_DIR + "/" + fname + ".pkl")
    #%%
        #print( df1[col].value_counts() )