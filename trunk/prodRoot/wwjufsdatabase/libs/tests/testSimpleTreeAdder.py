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


def sendMailMobile(filePath, parentId, itemName):
    f=open(filePath,'rb')
    test3 = f.read()
    f.close()

    params = urllib.urlencode({'itemName':itemName, 'treeRoot': parentId,'itemText': 'maildisk.maildisk@gmail.com', 'itemFile': test3,'username':'username','passwd':'passwd'})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    conn = httplib.HTTPConnection("127.0.0.1:9901")
    conn.request("POST", "/apps/tree/addItem.py", params, headers)
    response = conn.getresponse()
    print response.read()
    conn.close()

    
sendMailMobile('d:\\mini.usb0',0,'good upload item example')