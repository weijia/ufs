import os.path
import cherrypy
from cherrypy.lib.static import serve_file
#import sqlite3
import localLibs.thumb.thumbInterface as thumbLib
#from desktopApp.lib.transform import *
#import uuid
#import logging
#import pymedia.muxer

import wwjufsdatabase.libs.utils.transform as transform


#gAppPath = 'd:/tmp/fileman/'
#gThumbPath = os.path.join(gAppPath, 'thumb')

#misc.ensureDir(gAppPath)
#misc.ensureDir(gThumbPath)

#import wwjufsdatabase.libs.shove.shoveClientV5 as shoveClient
#thumbDb = libs.cache.shoveClient.Shove()

'''
class simpleSysUser:
    def getUserName(self):
        return 'system.default'
    def getPasswd(self):
        return 'simplePass'

'''
def getProdRoot():
    c = os.getcwd()
    while c.find('prodRoot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'prodRoot')


import wwjufsdatabase.libs.services.servicesV2 as service

class Root:
    def __init__(self):
        self.existingIconRelativePath = 'wwjufsdatabase\\webapproot\\static\\icons\\'
        self.prodRootPath = getProdRoot()
        self.req = service.req()
        
    @cherrypy.expose
    def thumb(self, path):
        #print path
        thumbP = self.getThumb(path)
        #print thumbP
        if thumbP is None:
            return None
        ext = thumbP.split('.')[-1]
        typeMapping = {'jpg':'image/jpeg', 'jpeg':'image/jpeg', 'png':'image/png', 'bmp':'image/bmp'}
        t = typeMapping[ext]
        return serve_file(thumbP,content_type=t)
        
    def getThumb(self, fullPath):
        path = transform.transformDirToInternal(fullPath)
        '''
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
        '''
        if True:
            #print path
            if os.path.isdir(path):
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'folder-images-icon.png')
            ext = path.split('.')[-1].lower()
            newPath = thumbLib.getThumb(path)
            if not (newPath is None):
                return newPath
            sup = ['doc','zip','wav','xls','txt','rar', 'pdf', 'ppt']
            #picSup = ['flv','mov','avi','rm','rmvb','jpg','jpeg','png','gif','bmp','wmv','mp4','3gp','mpg','mpeg', 'exe']

            if ext in sup:
                #print os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\%s.png'%ext)
            else:
                return os.path.join(self.prodRootPath,self.existingIconRelativePath+'online\\512px\\_page.png')
            

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': '../../site.log',
                            'log.screen': True,
                            'engine.autoreload_on' : True,
                            'server.socket_port' : 8805,})
    cherrypy.quickstart(Root(), '/')