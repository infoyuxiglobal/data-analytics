# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 10:14:25 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""

import os, sys, time, pprint, dask
import dask.dataframe as dd
import dask.distributed #even though not explicitely used it sets up some config options as side effect...


def load_define( data_dir, subset_fun ) :
    #%%
    #checkins_df = dd.read_hdf( data_dir + 'gowalla_checkins.hdf5', key='data' )
    checkins_df_0 = dd.read_csv( data_dir +  'Gowalla_totalCheckins.txt',
                                 delimiter="\t", names=['user_id', 'checkin_ts', 'lat', 'lon', 'location_id'],
                                 parse_dates = ["checkin_ts"] )

    chins1 = subset_fun( checkins_df_0[["user_id", "location_id", "checkin_ts"]] )

    #chins2 = chins1.merge( chins1, on="location_id" )
    chins1 = chins1.set_index('location_id')
    chins2 = chins1.join( chins1, lsuffix='_x', rsuffix='_y' )

    chins3 = chins2[ chins2.checkin_ts_x < chins2.checkin_ts_y ]
    #%%

    chins4 = ( chins3.reset_index()
                     [['location_id', 'user_id_x', 'user_id_y']]
                     .drop_duplicates()
                     .groupby(["user_id_x", "user_id_y"])
                     .agg( {"location_id" : "count"})
                     .rename( columns = { "location_id" : "location_count" } )
                     .reset_index() )


    q999 = chins4['location_count'].quantile( 0.999 )

    chins5 = chins4[ chins4.location_count > q999 ]
    #%%
    return chins1, chins4, q999, chins5

def test():
    #%%
    subset_fun= lambda dd0 : subset( dd0, 100, 2 )
    #%%
def main( ) :
    #%%
    if os.name == 'nt' :
        data_dir = "C:/_DATA/experimentation/"
    else :
        data_dir = "./"
        #%%
    pprint.pprint( dask.config.config )

    pct_of_input_data = float(sys.argv[1])
    print( "Running on %.0f%% of data" % pct_of_input_data )

    subset_fun = lambda dd0 : subset( dd0, 100, pct_of_input_data  )

    ( chins1,
      chins4,
      q999,
      chins5 ) = easy_time_it( lambda : load_define(data_dir, subset_fun),
                               "connecting to file and defining chins5" )
    size1 = easy_time_it( lambda : len(chins1), "computing size of initial dataset" )
    print( "len(chins1) = %d\n" % size1 )
    q999   = easy_time_it( lambda : q999.compute(), "computing q999" )
    chins5 = easy_time_it( lambda : chins5.compute(), "computing chins5" )

    print( "\n", chins5.sort_values('location_count', ascending=False).head() )


def subset( dd0, mod, h ) :
    return dd0[ dd0.location_id % mod < h ]

def easy_time_it( fun, msg = "" ) :
    t0 = time.clock()
    result = fun()
    t1 = time.clock( )
    print( "Time elapsed " + msg  +  " : %.3f s" % (t1 - t0) )
    return result


if __name__ == "__main__" :
    main()