import dbus.service
import localLibSys
import localLibs.logWin.dbusServices.dbusServiceBase as dbusServiceBase
import wwjufsdatabase.libs.ufsDb.ufsDbSingleUser as ufsDbSingleUser
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.thumb.thumbInterface as thumbLib
import wwjufsdatabase.libs.utils.misc as misc
import os
import uuid

gAppPath = 'd:/tmp/fileman/'
gThumbPath = os.path.join(gAppPath, 'thumb')

misc.ensureDir(gAppPath)
misc.ensureDir(gThumbPath)

INTERFACE_NAME = 'com.wwjufsdatabase.thumbService'

class simpleSysUser:
    def getUserName(self):
        return 'system.default'
    def getPasswd(self):
        return 'simplePass'

def getProdRoot():
    c = os.getcwd()
    while c.find('prodRoot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'prodRoot')

class thumbService(dbusServiceBase.dbusServiceBase):
    #The following function declaration is just a sample of overiding __init__ of class dbus.service.Object
    def __init__(self, sessionBus, objectPath):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        sessInst = simpleSysUser()
        dbSysInst = ufsDbSingleUser.dbSysSmart(sessInst)
        
        self.thumbDb = dbSysInst.getDb('thumbNew')
        self.pathDb = dbSysInst.getDb('pathNew')
        self.uuidDb = dbSysInst.getDb('uuidNew')
        self.existingIconRelativePath = 'wwjufsdatabase\\webapproot\\static\\icons\\'
        self.prodRootPath = getProdRoot()

    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='s')
    def getThumb(self, fullPath):
        path = transform.transformDirToInternal(fullPath)
        if not os.path.exists(path):
            print path.encode("gbk", "replace"), " not exist"
            raise KeyError
        try:
            u = unicode(self.pathDb[path][0])
        except KeyError:
            u = unicode(uuid.uuid4())
            self.pathDb[path] = u
            self.uuidDb[u] = path
        newPath = None
        try:
            #raise "no"
            newPath = self.thumbDb[u][0]
        except KeyError:
            #print path
            if os.path.isdir(path):
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'folder-images-icon.png')
            ext = path.split('.')[-1].lower()
            sup = ['doc','zip','wav','xls','txt','rar', 'pdf', 'ppt']
            picSup = ['flv','mov','avi','rm','rmvb','jpg','jpeg','png','gif','bmp','wmv','mp4','3gp','mpg','mpeg', 'exe']

            if ext in sup:
                #print os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
            if not (ext in picSup):
                #print os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
            newPath = thumbLib.getThumb(path, gThumbPath)
            if newPath is None:
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
            newPath = transform.transformDirToInternal(newPath)
            self.thumbDb[u] = newPath
            #thumbFile = libs.thumb.picThumbGenerator.returnThumbString(path)
            #files.serveStringFile(thumbFile, path)
            #files.serve(path)
            
        print 'returnning:',newPath
        return newPath
