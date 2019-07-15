import datetime
from flask import session,make_response
def writeTofile(username):
    f= open('data.txt','a',encoding='utf-8')
    dat=str(datetime.datetime.now())
    ftext= username+":"+dat+"\n"
    f.write(ftext)
def sess(username,remember):
    if remember:
        session['rexinauname'] = username
    else:
        resp=make_response('Mycookie')
        resp.set_cookie('rexinauname',username)





writeTofile('reza')