import dbus.service
import dbusServiceBase
import localLibSys
#import localLibs.windows.changeNotifyThread as changeNotifyThread
import localLibs.logWin.fileTools as fileTools
import localLibs.collection.objectDatabase as objectDatabase
import time
import appStarterForDbusTest
import wwjufsdatabase.libs.utils.transform as transform
import os
from localLibs.logSys.logSys import *

DELAY_SUBMIT_TIME = 10#(10 * 60)

INTERFACE_NAME = 'com.wwjufsdatabase.collectionService'

class taskManagerProxy:
    def started(self, appAndParam):
        return False
    def start(self, appAndParam):
        print 'start ', appAndParam


class collectionService(dbusServiceBase.dbusServiceBase):
    def __init__(self, sessionBus, objectPath, cfg):
        dbus.service.Object.__init__(self, sessionBus, objectPath)
        self.freqUpdatedList = {}
        self.objDb = objectDatabase.objectDatabase()
        self.taskMan = taskManagerProxy()
        self.registeredCallback = {}
        self.monitoring = {}
        self.cfg = cfg
    
    def addItem(self, collectionId, itemUrl):
        '''
        Add new item and start handler task if needed
        An item with the same itemUrl will be treated as a new item and will have a new UUID
        '''
        print 'calling addItem:', itemUrl
        '''
        #Check if the item is already in collection?
        if not self.objDb.getCollection(collectionId).updated(itemUrl):
            #If it is and it is the same as in the collection, return
            return
        '''
        #print '---------------------real adding item'
        #Update the item info for the item
        self.objDb.getCollection(collectionId).updateObj(itemUrl)
        #Check if the task is already started
        if not self.taskMan.started(self.registeredCallback[collectionId]):
            #If the task is not started, start it.
            self.taskMan.start(self.registeredCallback[collectionId])
        

        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='sssb', out_signature='')
    def notify(self, collectionId, itemUrl, action, frequentlyChanged):
        '''
        Add new item or updated item to collection, if changeNotification is 
        True, the item will not be submitted until certain time period passed
        '''
        print collectionId, itemUrl, action, frequentlyChanged
        if os.path.isdir(os.path.join(collectionId, itemUrl)):
            print 'dir, ignore:', os.path.join(collectionId, itemUrl)
            return
        itemUrl = "file:///"+transform.transformDirToInternal(os.path.join(collectionId, itemUrl))
        collectionId = str(collectionId)
        #Check if the item is already in collection
        col = self.objDb.getCollection(collectionId)
        if not self.freqUpdatedList.has_key(collectionId):
            self.freqUpdatedList[collectionId] = {}
        if col.exists(itemUrl):
            #Check if it is updated, if it is already in collection
            cl("item exists in col:", itemUrl)
            if col.updated(itemUrl):
                #If it is updated, add the item to frequent update item list
                #and wait for time out to add it
                cl("item updated in col:", itemUrl)
                self.freqUpdatedList[collectionId][itemUrl] = time.time()
            #Otherwise (the item is not updated), igonor
            else:
                pass
        else:
            if (not self.freqUpdatedList[collectionId].has_key(itemUrl)) and (not frequentlyChanged):
                #If the item is not in collection, and it will not change soon (means
                #the item will not be treated as frequently changed
                cl("add new item")
                self.addItem(collectionId, itemUrl)
            else:
                #Otherwise, add it to watching list
                cl("add to watch list")
                self.freqUpdatedList[collectionId][itemUrl] = time.time()
        
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='s', out_signature='')
    def timerEvent(self, collectionId):
        collectionId = transform.transformDirToInternal(collectionId)
        self.commitCollection(collectionId)
        
    def commitCollection(self, collectionId):
        '''
        TimerEvent was triggered to check if frequently changed items are now stable
        '''
        print 'commiting files'
        #Get new timestamp
        curSeconds = time.time()
        itemNeedRemove = []
        #Check all items in frequently updated item list for inserting
        for i in self.freqUpdatedList[collectionId].keys():
            #Check the item
            if self.freqUpdatedList[collectionId][i] + DELAY_SUBMIT_TIME < curSeconds:
                #If it is not modified in certain period of time
                self.addItem(collectionId, i)
                #itemNeedRemove.append(i)
                del self.freqUpdatedList[collectionId][i]
            else:
                #If it is modified again, do not process it
                print collectionId, self.freqUpdatedList[collectionId][i] + DELAY_SUBMIT_TIME, curSeconds
                continue
        '''
        for i in itemNeedRemove:
            del self.freqUpdatedList[i]
        ''' 
            
    @dbus.service.method(dbus_interface=INTERFACE_NAME,
                         in_signature='ss', out_signature='s')
    def register(self, dir2Monitor, callbackAppAndParam):
        dir2Monitor = transform.transformDirToInternal(dir2Monitor)
        if self.monitoring.has_key(dir2Monitor):
            return "Already registered"
        self.registeredCallback[dir2Monitor] = callbackAppAndParam
        pa = fileTools.findFileInProduct('dirMonitorV2.py')
        ru = [pa, '-p', "%s"%dir2Monitor]
        print ru
        appStarterForDbusTest.startAppFromDbus(ru)
        return "OK"

        
        
def getServiceObj(sessionBus, objectPath):
    return collectionService(sessionBus, objectPath)