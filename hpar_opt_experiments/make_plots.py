# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 14:41:46 2018

@author: Mateo
"""
#%%
import pandas as pd
import seaborn as sns

DATA_DIR=r"C:/Users/Mateo/Documents/_TRABAJO\Yuxi\Hyper_par_opt/"
#%%
df0 = pd.read_hdf( DATA_DIR + "df_gen.hdf", "a/" )
#%%
df0['best_so_far'] = df0.groupby( 'trial' )["fun_val"].apply( lambda x : x.cummax() )
#%%
df0.head(400)
#%%
def compute_percentiles( grp ) :
    pct01 = grp["best_so_far"].quantile(0.01)
    pct05 = grp["best_so_far"].quantile(0.05)
    return pd.DataFrame( { "pct01" : [ pct01 ], "pct05" : [ pct05 ] } )
#%%
df = df0.groupby( 'eval_cnt' ).apply( compute_percentiles )
#%%
#df0["pct01"] = df0.groupby( 'eval_cnt' ).apply( lambda grp : x.quantile(0.01) )
#%%
#df0["pct10"] = df0.groupby( 'eval_cnt' )["best_in_trial"].apply( lambda x : x.quantile(0.10) )

#%%
#ser = df0[df0.eval_cnt ==30]["best_in_trial"]
trial_idx=0
#%%
def plot_one_trial( df0, trial_idx ) :
    #%%
    df1 = df0[ df0.trial == trial_idx]
    #df1.plot( x='eval_cnt', y='fun_val', kind='scatter')
    sns.scatterplot( data=df1, x='eval_cnt', y='fun_val' )
    #%%