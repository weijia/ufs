'''
Created on Nov 4, 2011

@author: Richard
'''

#-*-coding:utf-8-*-

import urllib
import httplib

def sendMailMobile(filePath):
    f=open(filePath,'rb')
    test3 = f.read()
    f.close()

    params = urllib.urlencode({'mailTo': 'maildisk.maildisk@gmail.com', 'uploadFile': test3})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    conn = httplib.HTTPConnection("6.macrosoft.sinaapp.com")
    conn.request("POST", "/mailSender.php", params, headers)
    response = conn.getresponse()
    conn.close()
    print response.read()

sendMailMobile('E:\\apps\\tools\\dns.txt')