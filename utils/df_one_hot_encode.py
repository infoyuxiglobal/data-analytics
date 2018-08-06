# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 10:23:02 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""


#%%
from collections import defaultdict
import re
#%%

class DfOneHotEncoder :
    """An encoder for turning each of a set of categorical columns
    into several binary columns, one for each distinct value of the original column.
    For instance, if column A  has three distinct values, x, y and z, in the training
    set (passed to fit) then the result of transform on any data set containing an A
    colu,m will have three columns binary columns  A__x , A__y, A__z.
    Rows for which A has a value not seen during the fit face or a NaN, will be
    contain all 0's in the transform phase."""

    def __init__(self, cols ) :
        self.cols = cols

        self.vals_by_col = defaultdict( list )


    def fit(self, df ) :

        for col in self.cols :
            self.fit_col( df, col )


    def fit_col( self, df, col ) :

        val_cnts = df[col].value_counts().sort_values(ascending=False)
        #type( val_cnts )

        if len(val_cnts) > 7 :
            print(f"Warning: col={col} has {len(val_cnts)} distinct values.")

        for val in val_cnts.index :

            norm_val = re.sub( '[^A-Za-z0-9_]', '_', val.lower(),
                               flags=re.IGNORECASE )
            norm_val = re.sub( '_+', '_', norm_val )

            self.vals_by_col[ col ].append( (val, norm_val) )

        # Detect collisions
        tmp_dict = defaultdict( list )
        for val, norm_val in self.vals_by_col[col] :
            tmp_dict[norm_val].append( val )

        for val_lst in tmp_dict.values( ) :
            assert len(val_lst) == 1, ( f'Collision detected for col={col} :'
                f' all values in {val_lst} get encoded to the same normalized value' )


    def transform( self, df, drop_old=False) :

        for col in self.cols :

            for val, norm_val in self.vals_by_col[col] :
                new_col = col + "__" + norm_val
                df[new_col] = (df[col] == val)

            if drop_old :
                del df[col]

        return df
    #%%
def test( df0, self ) :
    #%%
    df = df0
    col = "name_contract_type"
    enc = DfOneHotEncoder(  [ col for col in cat_vars_0.index
                              if  col != 'organization_type' ] )
    enc.fit( df )
    #%%

