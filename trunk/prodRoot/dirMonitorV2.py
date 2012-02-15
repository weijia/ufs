import dbus.service
import dbus
from optparse import OptionParser
import os
import time
import win32file
import win32con
import wwjufsdatabase.libs.utils.transform as transform


ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}

BUS_NAME_NAME = 'com.wwjufsdatabase.collectionService'
INTERFACE_NAME = 'com.wwjufsdatabase.collectionService'
OBJ_NAME = '/service'

def checkDirChanges(path_to_watch, busname = BUS_NAME_NAME, interfacename = INTERFACE_NAME, objname = OBJ_NAME):
    path_to_watch = transform.transformDirToInternal(os.path.abspath (path_to_watch))
    need_to_quit = False
    print "Watching %s at %s" % (path_to_watch, time.asctime ())
    hDir = win32file.CreateFile(
        path_to_watch,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    cnt = 0
    bus = dbus.SessionBus()
    proxy = bus.get_object(busname, objname)
    ###############################################
    #Scan for existing files
    ###############################################
    for i in os.walk(path_to_watch):
        print i
        for j in i[2]:
            fullPath = transform.transformDirToInternal(os.path.join(i[0], j))
            #print fullPath
            proxy.notify(path_to_watch, fullPath, "Existing", False, dbus_interface = interfacename)

    while not need_to_quit:
#            print "new watch\n"
        results = win32file.ReadDirectoryChangesW(
            hDir,
            1024*256,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME
            | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
            | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
            | win32con.FILE_NOTIFY_CHANGE_SIZE
            | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
            | win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
        )
        if not need_to_quit:
            for action, file in results:
                #full_filename = os.path.join (self.path_to_watch, file)
                #print full_filename, ACTIONS.get (action, "Unknown")
                #callback(self.path_to_watch, file, ACTIONS.get (action, "Unknown"))
                print 'filechanged called:', path_to_watch, file, ACTIONS.get (action, "Unknown")
                proxy.notify(path_to_watch, file, ACTIONS.get (action, "Unknown"), True, dbus_interface = interfacename)
    
    
if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-p", "--path", action="store",help="path which need to be monitored")
    parser.add_option("-b", "--busname", action="store",help="bus name for notifying", default = BUS_NAME_NAME)
    parser.add_option("-i", "--interface", action="store", help="interface for notifying", default = INTERFACE_NAME)
    parser.add_option("-o", "--objname", action="store", help="object for notifying", default = OBJ_NAME)
    (options, args) = parser.parse_args()
    checkDirChanges(options.path, options.busname, options.interface, options.objname)