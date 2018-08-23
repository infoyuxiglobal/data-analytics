# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 13:53:11 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""
import pickle
import os

class Memoizer :
    """class to wrap a function and memoize it
    periodically stores evaluations to disk"""

    def __init__(self, fun, memoization_path, refresh_every=10 ) :

        self._fun = {}
        self._cache = {}
        self._memoization_path = memoization_path
        self._refresh_every = refresh_every

        if not os.path.exists( memoization_path ) :
            print( "Memoizer: Making dir: " + memoization_path )
            os.mkdir( memoization_path )


        self._memos_file = memoization_path + '/memos.pkl'
        self._new_evals_cnt = 0

        if os.path.exists( self._memos_file ) :
            with open( self._memos_file, "rb" ) as f_in :
                self._cache = pickle.load( f_in )
                print( "Memoizer: Loaded cache from: %s  with %d records " %
                      (self._memos_file, len(self._cache)) )
        else :
            print( self._memos_file, "does not exist. Will be created after %d new evaluations"
                  % self._refresh_every )

    def __call__( self,  param_dic ) :

        hex_hash = md5( str( tuple(param_dic.items()) ).encode("utf8") ).hexdigest()

        if hex_hash in self._cache :
            return self._cache[ hex_hash ]["fun_val"]

        else :
            t0 = time.clock()
            fun_val = self._fun( param_dic )
            elapsed = time.clock() - t0
            self._new_evals_cnt += 1

            record = { "elapsed" : elapsed,
                        "params" : list( param_dic.items() ),
                        "fun_val" : fun_val  }

            self._cache[hex_hash] = record

            if self._new_evals_cnt % self.refresh_every_ == 0 :
                print( "Refreshing memos file" )
                self.refresh_memos_file()

    def refresh_memos_file( self ) :
        with open( self._memos_file, "wb" ) as f_out :
            pickle.dump( self.cache, f_out )



def transform_json_memos( memoization_path ) :

    #%%
    memoization_path = r"C:\_DATA\experimentation\HC_Default_Risk\xgboost_memo0.05\json_memos_bkup"
    json_files = [f for f in os.listdir( memoization_path ) if f.endswith(".json") ]

    ret_dic = {}

    for memo_file in json_files :
        full_path =  memoization_path + "/" + memo_file
        with open( full_path, "rt", encoding="utf8" ) as f_in :
            json_obj = json.loads( f_in.read() )
            json_obj["fun_val"] = json_obj["auc"]
            del json_obj["auc"]
            key = memo_file[:-5]  #remove .json from the end
            ret_dic[key] = json_obj

    with open( memoization_path + '/../memos.pkl', "wb" ) as f_out :
        pickle.dump( ret_dic, f_out )
    #%%
    return ret_dic
    #%%


