# -*- coding: utf-8 -*-
"""
Created on Thu May  3 15:27:15 2018

@author: mrestrepo
 
Motivation

Talk about lime 

Problems with scalability 

Our proposal 

Worked out example 

Extensions: 
    - XGBoost 
    - multiclass 
"""
#%%

from sklearn.ensemble import RandomForestClassifier

import pandas as pd
import math 

from tcxp import rf_explain 

#%%
    
def test() :
    #%%
    train_df = pd.read_csv( "c:/tmp/titanic/train.csv" )

    train_df, train_Y = preproc( train_df )
    #%%
    rfc = RandomForestClassifier( n_estimators=100, max_depth=4 )
    rfc.fit( train_df, train_Y)
    train_pred = rfc.predict( train_df )
    accu = (train_pred == train_Y).sum() / len( train_pred )
    #%%
    E, p0 = rf_explain( rfc, train_df )
    #%%
   
    
def preproc( train_df ) : 
    #%%
    train_Y = train_df["Survived"]
    
    train_df["age_unknown"] = 1.0 * train_df["Age"].isna() 
    train_df["Age"].fillna( -99, inplace=True ) 
    
    del train_df["Survived"]
    
    del train_df["Name"]
    train_df["sex_female"] = 1.0* ( train_df["Sex"] == "female")    
    del train_df["Sex"]
    
    train_df["Embarked_C"] = 1.0 * (train_df["Embarked"] == "C" )
    train_df["Embarked_S"] = 1.0 * (train_df["Embarked"] == "S" )
    
    del train_df["Embarked"]
    
    del train_df["Ticket"] # TODO : maybe extract something from here
    del train_df["Cabin"] # TODO : maybe extract something from here
    del train_df["PassengerId"]
    #def extract_cabin_letter( cabin ) : 
    #    return "." if safe_isnan(cabin)  else cabin[0]
    
    #train_df["Cabin"].apply( extract_cabin_letter)
    
    #%%
    return train_df, train_Y
    #%%

def safe_isnan( x ) : 
    return type(x) is float and math.isnan(x)

def freq_table( series, count_col = "count" ) : 
    return pd.crosstab( series, columns=count_col )
