# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 18:13:58 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""
import turicreate as tc
import turicreate.aggregate as agg

#%%
import time

PCT = 100

SHOW_COUNTS = True

def main( pct, show_counts ) :
    t0 = time.clock()

    sf = ( tc.SFrame.read_csv( 'Gowalla_totalCheckins.txt',
                             delimiter='\t', header=False )
                   .rename( {'X1' : 'user_id',
                             'X2' : 'checkin_ts',
                             'X3' : 'lat',
                             'X4' : 'lon',
                             'X5' : 'location_id'} ) )

    sf2 = sf[ sf['location_id'] % 100 < pct ]

    checkins = sf2[["user_id", "location_id", "checkin_ts"]]

    if show_counts :
        print( 'checkins has: %d' % len(checkins) )

    chin_ps = ( checkins.join( checkins, on = 'location_id' )
                        .rename( {'checkin_ts' : 'checkin_ts_ee',
                                  'checkin_ts.1' : 'checkin_ts_er',
                                  'user_id' : 'stalkee' ,
                                  'user_id.1' : 'stalker' ,
                                  }) )

    if show_counts :
        print( 'chin_ps has: %d' % len(chin_ps) )

    t1 = time.clock()
    print("time: ",  t1 - t0 )

    pairs_filtered = chin_ps[ (chin_ps['checkin_ts_ee'] < chin_ps['checkin_ts_er']) &
                       (chin_ps['stalkee'] != chin_ps['stalker']) ]

    if show_counts:
        print( 'pairs_filtered has: %d' % len(pairs_filtered) )

    t1 = time.clock()
    final_result = ( pairs_filtered[[ 'stalkee', 'stalker', 'location_id']]
                     .unique()
                     .groupby( ['stalkee','stalker'] ,
                               {"location_count" : agg.COUNT })
                     .topk( 'location_count', k=5, reverse=False )
                     .materialize() )


    t2 = time.clock()

    print(final_result, "\n Computation Time = ",  t2 - t1 )

def pandas(checkins_df):
    #%%
    checkins_by_loc = (checkins_df[['user_id', 'checkin_ts', 'location_id']]
                      .set_index('location_id') )

    chin_pairs = checkins_by_loc.join( checkins_by_loc, lsuffix='_ee', rsuffix='_er' )

    pairs_filtered = (chin_pairs[(chin_pairs.checkin_ts_ee < chin_pairs.checkin_ts_er) &
                                 (chin_pairs.user_id_ee != chin_pairs.user_id_er )]
                          .rename( columns= {"user_id_er" : "stalker",
                                             "user_id_ee" : "stalkee" })
                          .reset_index()
                          [["stalkee", "stalker", "location_id"]] )

    final_result = ( pairs_filtered.drop_duplicates()
                     .groupby(["stalkee", "stalker"])
                     .agg( {"location_id" : "count"})
                     .rename( columns = { "location_id" : "location_count" } )
                     .sort_values('location_count', ascending=False) )

    #%%
    return final_result




main( PCT, SHOW_COUNTS )
