import localLibSys
import os
import time
import desktopApp.lib.compress.zipClass as zipClass

'''
curArchive = zipClass.ZFile('d:/tmp/test.zip', 'w')
curArchive.addfile('D:/tmp/libdbus-1.dll', 'libdbus-1.dll')

curArchive.close()
'''

def getTimeTuple(seconds):
    t = time.localtime(seconds)
    return (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

curArchive = zipClass.ZFile('d:/tmp/test.zip', 'r')
print curArchive.zfile.getinfo('libdbus-1.dll').date_time
print type(curArchive.zfile.getinfo('libdbus-1.dll').date_time)
print "last modified: %s" % time.ctime(os.stat('D:/tmp/libdbus-1.dll').st_mtime)
print getTimeTuple(os.stat('D:/tmp/libdbus-1.dll').st_mtime)
print getTimeTuple(os.stat('D:/tmp/libdbus-1.dll').st_mtime) == curArchive.zfile.getinfo('libdbus-1.dll').date_time