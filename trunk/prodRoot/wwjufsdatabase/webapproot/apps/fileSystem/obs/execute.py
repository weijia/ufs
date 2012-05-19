import libSys
import libs.utils.webUtils as webUtils
import os
#import subprocess
import localLibs.logWin.appStarterFromDbus as dbusStarter

if __name__=='__main__':
    #Get request param: collectionId, start, cnt
    param = webUtils.paramWithDefault({u"path":None})
    path = param["path"]
    print path.encode('utf8','replace')
    #os.system('"'+path+'"')
    #subprocess.Popen('"'+path+'"',shell=True)
    #os.spawnv(P_NOWAIT, '"'+path+'"')
    try:
        ext = os.path.splitext(path)[1]
    except:
        ext = ''
    if (ext in ['.bat', '.py']):
            dbusStarter.startAppFromDbus([path])
            raise "stop here"
    else:
        os.startfile('"'+path+'"')
        #raise "stop there"