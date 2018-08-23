# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 10:58:57 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""
from collections import OrderedDict

class InstFunEvaluator :
    """Instrumented function evaluator"""

    def __init__( self, fun, param_grid_dic, log_level=0 )  :
        """Initialize evaluator function and param_grid
        fun should be a function taking a single argument (implementing a dict interfase) and
            returning a float.
        param_grid_dic should an ordered dic with keys being parameter names
        each value in should be an array of valid values for the i-th argument of fun """

        #n_params = len(param_grid)
        assert isinstance( param_grid_dic, OrderedDict ), "param_grid_dic should be an ordered dict"

        self._fun = fun
        self._param_grid  = list( param_grid_dic.values() )
        self._param_names = list( param_grid_dic.keys() )

        self._n_params = len( self._param_grid )

        #self._eval_cnt = 0
        self._eval_log = []
        self._log_level = log_level

    def from_idxs(self, x_idxs, extra=None ) :
        """Evaluate self.fun on parameters given by indices into each value of the
        param grid, that is for the d-th parameter use the x_idxs[d] value
        for the corresponding valid range of values"""

        param_dic  = { self._param_names[d] : self._param_grid[ d ][ x_idxs[d] ]
                       for d in range( self._n_params) }

        return self.eval_fun( param_dic, extra )

    def from_vals( self, val_arr, extra=None ) :
        param_dic = { name : val
                      for name, val in zip(self._param_names, val_arr ) }

        return self.eval_fun( self, param_dic, extra )

    def eval_fun(self, param_dic, extra=None ) :

        fun_val = self._fun( param_dic )

        if self._log_level > 0  :
            print( param_dic, fun_val)


        #self._eval_cnt += 1
        eval_record = { "eval_cnt" : self.eval_cnt(),
                        "pars"     : param_dic,
                        "extra"    : extra,
                        "fun_val"  : fun_val  }

        self._eval_log.append( eval_record )

        return fun_val


    def eval_cnt( self  ) :
        """Return total number of function evaluations so far"""
        return len( self._eval_log )

    def eval_log( self ) :
        """Return a list of dicts containing details about evaluations so far"""
        return self._eval_log

    def idxs_to_xs( self, x_idxs ) :
        return [ self._param_grid[idx] for idx in x_idxs ]
