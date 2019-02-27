import pandas as pd

# the following file was created with du . > space.txt  
with open( "C:/Users/mrestrepo/Documents/space0.txt" ) as f_in : 
    lines = f_in.readlines() 
        
recs = []

for line in lines : 
    ps = line.split() 
    size = int( ps[0] )
    path = "".join( ps[1:] )[1:] # drop first char that is just '.' always... 
    pieces = path.split("/" )
    depth  = len(pieces)
    
    recs.append( [size, 
                  path, 
                  depth-1, 
                  pieces[0],
                  pieces[1] if depth > 1 else "",
                  pieces[2] if depth > 2 else "", 
                  pieces[3] if depth > 3 else ""] )
    
    
df = pd.DataFrame( recs, columns = ['size_kb', 'full_path', 'depth', 'l0', 'l1', 'l2', 'l3' ] )
df1 = df[ (df.depth > 0) & (df.depth <= 3) & (df.size_kb != 0)]


df1.size_kb.sum()
df1[ df1.depth == 2].size_kb.sum()

du_df = df1.sort_values( ['l1', 'l2', 'l3']).reset_index( drop = True ) 

#du_df.to_csv('disk_usage_0.csv', index=False)


# nested sizes at level > 2 
nested_3 = ( du_df[du_df['l3'] !=  '' ]
                .groupby( ['l1', 'l2'])
                .agg( {'size_kb' : 'sum'} )
                .reset_index() 
                .rename( columns={'size_kb' : 'nested_kb'} ) ) 

non_nested_3 = nested_3.merge( du_df[ du_df.depth == 2 ]
                             [['l1', 'l2', 'size_kb']]
                             .rename( columns= { 'size_kb' : 'size_total_kb'} )                 
                            , how='outer' ).fillna( 0 )

non_nested_3['size_kb'] = non_nested_3['size_total_kb'] - non_nested_3['nested_kb']
non_nested_3['l3'] = '.'
non_nested_3['full_path'] = '/' + non_nested_3['l1'] + '/'  + non_nested_3['l2'] +'/.' 
non_nested_3['depth'] = 2 

du_df1 = pd.concat( [ du_df[du_df.depth != 2], 
                      non_nested_3.drop( ['nested_kb', 'size_total_kb'], axis=1) ],
                      sort=False ).sort_values( ['l1', 'l2', 'l3'] ) 

# nested sizes at level > 2 
nested_2 = ( du_df1[du_df1['l2'] !=  '' ]
                .groupby( ['l1'])
                .agg( {'size_kb' : 'sum'} )
                .reset_index() 
                .rename( columns={'size_kb' : 'nested_kb'} ) ) 

non_nested_2 = nested_2.merge( du_df1[ du_df1.depth == 1 ]
                             [['l1', 'size_kb']]
                             .rename( columns= { 'size_kb' : 'size_total_kb'} )                 
                            , how='outer' ).fillna( 0 )        

non_nested_2['size_kb'] = non_nested_2['size_total_kb'] - non_nested_2['nested_kb']
non_nested_2['l2'] = '.'
non_nested_2['l3'] = ''
non_nested_2['full_path'] = '/' + non_nested_2['l1'] + '/.'
non_nested_2['depth'] = 1 


du_df2 = ( pd.concat( [ du_df1[du_df1.depth != 1], 
                      non_nested_2.drop( ['nested_kb', 'size_total_kb'], axis=1) ],
                      sort=False )
              .sort_values( ['l1', 'l2', 'l3'] ) 
              .reset_index( drop=True ) )  

du_df2[['full_path', 'depth', 'size_kb', 'l1', 'l2', 'l3']
       ].to_pickle('disk_usage.pkl')


            #%%