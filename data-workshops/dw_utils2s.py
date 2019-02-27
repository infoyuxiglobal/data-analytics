# -*- coding: utf-8 -*-
"""
Created on Tue May  8 18:00:37 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""

import urllib.request
from urllib import parse
import ssl

# Going functional..

print( "Loading dw_utils2 module (v. 20180625)" )

def create_submitter( host='localhost', port=80, user='mateini', token='', ws_key='dw1' ) :

    print( "Creating submitter function Submitting test question to verify connection." )

    # construct the closure we are going to return
    def submit( question_id, answer, echo=True, ac_reload= False) :
        return submit_full( host, port, user, token, ws_key, question_id, answer, echo=echo )

    submit( 'Q00', 'test answer' )

    return submit

def submit_full( host, port, user, token, ws_key, question_id, answer, echo=True ) :
    if echo :
        print( '%s = %s' % (question_id, repr(answer)) )

    try :
        answer_enc = parse.quote( str(answer).strip() )
        user_enc   = parse.quote( str(user).strip().lower() )
        ws_enc     = parse.quote( str(ws_key).strip() )
        q_id_enc   = parse.quote( str(question_id).strip() )
        token_enc  = parse.quote( str(token).strip() )
        pre = "https" if port == 443 else "http"
        url = f'{pre}://{host}:{port}/v2/answer?w={ws_enc}&u={user_enc}&tk={token_enc}&q={q_id_enc}&t={answer_enc}'
        print( url ) 
        
        context = ssl._create_unverified_context()
        print( context )

        with urllib.request.urlopen(url, context=context) as response:
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
