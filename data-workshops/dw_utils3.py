# -*- coding: utf-8 -*-
"""
Created on Tue May  8 18:00:37 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""

import urllib.request
from urllib import parse
import os
#import requests

#import ssl
#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH'
# Going functional..

CERT_PATH = "./dw.cert"
#%%

print( "Loading dw_utils3 module (v. 20181113)" )

def create_submitter( host='localhost', port=80, user='mateini', token='', ws_key='dw1' ) :

    print( "Creating submitter function and submitting test question to verify connection." )

    # construct the closure we are going to return
    def submit( question_id, answer, echo=True, ac_reload= False) :
        return submit_full( host, port, user, token, ws_key,
                            question_id, answer, echo=echo, ac_reload=ac_reload)

    submit( 'Q00', 'test answer' )

    return submit

def submit_full( host, port, user, token, ws_key, question_id, answer,
                 echo=1, ac_reload=False ) :
    if echo :
        print( '%s = %s' % (question_id, repr(answer)) )

    try :
        answer_enc = parse.quote( str(answer).strip() )
        user_enc   = parse.quote( str(user).strip().lower() )
        ws_enc     = parse.quote( str(ws_key).strip() )
        q_id_enc   = parse.quote( str(question_id).strip() )
        token_enc  = parse.quote( str(token).strip() )
        ra = 1 if ac_reload else 0
        pre = "https" if port == 443 else "http"

        url = ( f'{pre}://{host}:{port}/v2/answer?w={ws_enc}&u={user_enc}'
                f'&tk={token_enc}&q={q_id_enc}&t={answer_enc}&ra={ra}' )
        if echo > 2 :
            print( url )
        #context = ssl._create_unverified_context()
        #context= ssl.SSLContext()
        #print( context )
        #print( "CCC", ctx, ctx.verify_mode, ctx.verify_flags )
        if not os.path.exists( CERT_PATH ) :
            raise RuntimeError( "Error: Certificate file not found at: " + CERT_PATH )

        with urllib.request.urlopen(url, cafile=CERT_PATH) as response:
        #with requests.get(url, verify=False) as response:

        #response = requests.get(url, verify=False)
        #if response :
            txt = response.read()
            if txt == b'Received Correct' :
                print( f'Answer for question {question_id} is correct \U0001F603' )
            elif txt == b'Received Incorrect' :
                print( f'Answer for question {question_id} is incorrect \U00002639' )
            elif txt == b'Received Undefined' :
                print( f'Correct Answer for question {question_id} is not yet defined.'
                        " Kindly ask Mateo to do it..." )
            else:
                raise ValueError( 'Received unexpected answer from server: %s' % txt )
        print( "" )

    except Exception as exc :
        print( exc )
