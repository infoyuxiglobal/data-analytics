# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 16:53:05 2018

@author: mrestrepo
"""


import pandas as pd
import numpy as np 
DATA_DIR="c:/_DATA/DW5/"
#%%

def main( ) : 
    #%%
    n = int( 1e6 ) 
    customer_df = customer(n) 
    
    customer_df.to_csv( DATA_DIR + 'customer.csv', sep=';', index=False ) 
    #%%
    bod_df = bod(n)
    #%%
    bod_df.to_csv( DATA_DIR + 'bod.csv', sep=';', index=False ) 
    #%%
    cs_df = credit_score( n )
    cs_df = cs_df[cs_df.cust_id % 10 == 1]
    cs_df.to_csv( DATA_DIR + 'credit_score.csv', sep=';', index=False ) 
    #%%
    
    #%%
    print( gen_create_table( 'customer', customer_df, pk='cust_id' ) ) 
    print( gen_create_table( 'credit_score', cs_df, pk='cust_id' ) )
    print( gen_create_table( 'bod', bod_df, pk='cust_id' ) )
    
    #%%
    m = 500 
    fn_out = "phones_subset.csv"
    phones_subset( customer_df.phone, m )
    #%%
    
    
def customer( n ) : 
    #%%
    with open( DATA_DIR + "/first-names.txt", encoding="utf8" ) as f_in  :
        first_names0 = [ line.strip() for line in f_in.readlines() ]
    #%%    
    with open( DATA_DIR + "/surnames.txt", encoding="utf8" ) as f_in  :
        last_names0 = [ line.strip() for line in f_in.readlines() ]
    
    #%%
    cities_df = pd.read_csv(  DATA_DIR + "/cities.txt" )
    
    #%%
    cities0 =  cities_df.city 
    city_2_st  = dict( zip( cities_df.city, cities_df.state) ) 
    #%% 
    cust_id = list( range(0,n) )
    
    first_names = np.random.choice( first_names0, n )
    last_names = np.random.choice( last_names0, n )
    
    city =  np.random.choice( cities0, n )
    
    state =  [ city_2_st[ci] for ci in city ]
    #%%
    phones = np.int64( np.random.uniform( 2e9, 7e9, size= n ) )
    #%%
    tier = np.random.choice( range(10), n )
    
    sales = np.round( np.random.lognormal( mean=8, sigma=1, size=n) * (tier + 1) ) 
    
    customer_df = pd.DataFrame( { 'cust_id' : cust_id, 
                               'first_name' : first_names, 
                               'last_name' : last_names, 
                               'city' : city, 
                               'state' : state,
                               'tier' : tier,
                               'phone' : phones,
                               'sales' : sales } )
    #%%
    return customer_df

def bod( n ) : 
    #%%
    cust_id = list( range(0,n) )
    age_days = np.int32( np.random.uniform( 365*16, 365*90, size= n ) )
    #%%
    bod_df = pd.DataFrame( {"cust_id" : cust_id, "age_days" : age_days } )
    #%%
    bod_df['today'] = pd.datetime.today() 
    #%%
    bod_df['bod'] =  bod_df['today'] - pd.to_timedelta( age_days, 'd' ) 
    #%%
    bod_df['bod']  = bod_df['bod'].dt.strftime( '%Y-%m-%d' )
    #%%
    return bod_df[['cust_id', 'bod']]


def credit_score( n ) : 
    #%%
    cust_id = list( range(0,n) )
    credit_score = np.int32( np.random.uniform( 500, 800, size= n ) )
    #%%
    return pd.DataFrame( {"cust_id" : cust_id, "credit_score" : credit_score } )
    #%%
    
  
def phones_subset( all_phones, m ) : 
    #%%
    phones_subset = [ str(ph) for ph in np.random.choice( all_phones, m ) ]
    #%% 
    query  = ( f"select * from customer\nwhere phone in (%s);" % 
                ", ".join( phones_subset ) )
    
    with open( "query_phone_in_500.sql", "w") as f_out : 
        print( query, "\n", file=f_out)
        
    #%%
    with open( "create_phone_subset.sql", "w") as f_out : 
        print( f"create temp table phones_subset (phone) as values " + 
          ", ".join( "(%s)" % id_ for id_ in phones_subset )  + ";", 
          file=f_out)
    #%%
    return # ids_subset, query
#%%
def test_write_create_table( employee_df ) : 
    #%%
    tbl_name = 'employee'
    df = employee_df
    #%%
    print( gen_create_table( tbl_name, df ) ) 
    #%%
    n= int(1e6)
    #%%
#%%
def gen_create_table( tbl_name, df, pk ) : 
    
    
    translate_dtype = {
            'int64' : 'BIGINT',
            'int32' : 'INT',
            'float64' : 'REAL',
            'object' : 'VARCHAR'}
    
    varchar_lens = { col_name :  (  '(%s)' % df[col_name].str.len().max()  if str(type_) == 'object' else '' ) 
                    for col_name, type_ in zip( df.dtypes.index, df.dtypes.values  )
                    }
    
    col_decls = [ f"{col_name} {translate_dtype[str(type_)]}{varchar_lens[col_name]}"
                  f"{' PRIMARY KEY' if col_name==pk else ''}"
                  for col_name, type_ in zip( df.dtypes.index, df.dtypes.values  ) ]
    
    col_decls_str = ",\n\t".join(col_decls) 
    
    return  f"CREATE TABLE {tbl_name} (\n\t{col_decls_str}\n);"
    