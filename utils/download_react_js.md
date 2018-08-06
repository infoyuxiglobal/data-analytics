# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:46:28 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""
import os
import requests
#%%
files = """css/reveal.css
css/theme/simple.css
lib/js/head.min.js
js/reveal.js""".split( "\n")

ver = "3.5.0"
local_prefix = "reveal.js" # directory to store files under
url_pref = "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/"

#%%

def mkdir_rec( dirname ) :
    ps = os.path.split( dirname )

    for i in range( len(ps) ) :
        partial = os.path.join( ps[ : (i+1)] )
        if not os.path.exists( partial ) :
            os.mkdir( partial )

def main() :
    #%%
    if not os.path.exists(  local_prefix ) :
        os.mkdir( local_prefix )
    #%%
    for fn in files :
        req_fn = url_pref + ver + "/" + fn
        print( req_fn )

        print( "Downloading from: " + req_fn )
        r = requests.get( req_fn  )

        local_fn = local_prefix + "/" + fn
        print( "Writing to: " + local_fn )
        dirname = os.path.dirname( local_fn )
        mkdir_rec( dirname )
        with open( local_fn, "w", encoding="utf8") as f_out :
            print( r.text, file=f_out )


    #%%

