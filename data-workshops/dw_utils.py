# -*- coding: utf-8 -*-
"""
Created on Tue May  8 18:00:37 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)
"""

import urllib.request
from urllib import parse 

class AnswerSubmitter : 

    def __init__( self, host='localhost', port=80, user='mateini' ) :
		
        self.host = host
        self.port = port 
        self.user = user 
        print( "AnswerSubmitter: v. 20180510 initialized. Submitting test question to verify connection." )
        self.submit( 'Q00', 'test_answer' ) 
        
    def submit( self,  question_id, answer, echo=True ) : 
        if echo : 
            print( '%s =' % question_id )
            print( repr(answer) )
            
        try :
            answer_enc = parse.quote( str(answer).strip() )
            user_enc = parse.quote( str(self.user).strip() )
            q_id_enc = parse.quote( str(question_id).strip() )
            
            url = f'http://{self.host}:{self.port}/answer?u={user_enc}&q={q_id_enc}&t={answer_enc}'
            with urllib.request.urlopen(url) as response:            
                txt = response.read()
                if txt == b'Received' : 
                    print( f'Answer for question {question_id} submitted successfully!' )
                else: 
                    raise ValueError( 'Received unexpected answer from server: %b' % txt )
                
        except Exception as exc : 
            print( exc )           
