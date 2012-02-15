import urllib
import httplib
'''
f=open('d:\\url.txt','rt')
test3 = f.read()
f.close()

params = urllib.urlencode({'mailTo': 'maildisk.maildisk@gmail.com', 'uploadFile': test3})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}

conn = httplib.HTTPConnection("wwjufsdatabase.appspot.com")
conn.request("POST", "/apps/mail/mailSender.py", params, headers)
response = conn.getresponse()
conn.close()
'''


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
