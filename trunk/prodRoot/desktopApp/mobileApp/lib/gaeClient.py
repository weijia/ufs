import httplib
import jsTreeDbNamedItemParser
import uuid
import urllib

class gaeClient:
    def __init__(self, username, password, server = "wwjufsdatabase.appspot.com"):
        self.username = username
        self.password = password
        self.server = server
    def rmItem(self, itemId, destFullPath):
        print 'Download %s to: %s'%(itemId, destFullPath)
        urllib.urlretrieve('http://'+self.server+'/apps/tree/deleteItem.py?itemId=%s&username=%s&passwd=%s'%(itemId,self.username,self.password), destFullPath)

    def addItemWithData(self, data, itemName, parentItem, itemId = None, itemDataId = None):
        import uuid
        if itemId is None:
            itemId = str(uuid.uuid4())
        if itemDataId is None:
            itemDataId = str(uuid.uuid4())
        paramDict = {'username': self.username, 'passwd':self.password, 'itemId':itemId, 'itemDataId':itemDataId,'itemName':itemName, 'treeRoot': parentItem}
        #print paramDict
        if not (data is None):
            paramDict['itemFile'] = data
        params = urllib.urlencode(paramDict)
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}

        conn = httplib.HTTPConnection(self.server)
        #print 'http request:',self.server
        conn.request("POST", "/apps/tree/addItem.py", params, headers)
        response = conn.getresponse()
        
        conn.close()
        '''
        results = urllib.urlopen('http://'+self.server+"/apps/tree/addItem.py", params).read()
        #print results
        
    def addItem(self, dataFileFullPath, itemName, parentItem, itemId = None, itemDataId = None):
        f=open(dataFileFullPath,'rb')
        test3 = f.read()
        f.close()
        self.addItemWithData(data, itemId, itemDataId)
        
    def updateItem(self, dataFileFullPath, itemId, itemDataId = None):
        f=open(dataFileFullPath,'rb')
        test3 = f.read()
        f.close()
        updateItemWithData(test3, itemId, itemDataId)
        
    def updateItemWithData(self, data, itemId, itemDataId = None):
        if itemDataId is None:
            itemDataId = str(uuid.uuid4())
        params = urllib.urlencode({'username': self.username, 'passwd':self.password, 'itemId':itemId, 'itemDataId':itemDataId, 'itemFile': data})
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        '''
        conn = httplib.HTTPConnection(self.server)
        conn.request("POST", "/apps/tree/updateItem.py", params, headers)
        response = conn.getresponse()
        conn.close()
        '''
        results = urllib.urlopen('http://'+self.server+"/apps/tree/updateItem.py", params).read()
        #print results
