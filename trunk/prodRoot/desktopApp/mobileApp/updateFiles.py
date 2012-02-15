import libSys
import objSync
import gaeItem
import localItem
import cfg
import os
import pprint

if __name__ == '__main__':
    #Read current state from disk
    c = cfg.cfg()
    settings = c.getSettings()
    gAppBaseDir = settings.get('rootDir', 'd:\\tmp\\syncFile')
    
    itemDict = settings.get('otherSettings', {})
    #pprint.pprint(itemDict)
    itemDict['workingDir'] = settings.get('workingDir', os.path.join(gAppBaseDir, 'working'))
    itemDict['legacyFilePath'] = settings.get('legacyFilePath', os.path.join(gAppBaseDir, 'legacy'))
    #itemDict['abnormalFilePath'] = settings.get('abnormalFilePath', os.path.join(gAppBaseDir, 'abnormal'))
    itemDict['tmpFilePath'] = settings.get('tmpFilePath', os.path.join(gAppBaseDir, 'tmp'))
    
    itemDict['treeDb'] = itemDict.get('treeDb', {})

    if not os.path.exists(itemDict['workingDir']):
        os.makedirs(itemDict['workingDir'])

    if not os.path.exists(itemDict['legacyFilePath']):
        os.makedirs(itemDict['legacyFilePath'])

    #if not os.path.exists(self.settings['abnormalFilePath']):
    #    os.makedirs(self.settings['abnormalFilePath'])
        
    if not os.path.exists(itemDict['tmpFilePath']):
        os.makedirs(itemDict['tmpFilePath'])

    #itemId = '1549e017-77c4-46da-81c2-8b3d04026ba1'
    g = gaeItem.gaeItem('3fe6382b-0219-40c7-add3-2f3b60aeb368', 'username', 'passwd', itemDict['tmpFilePath'], None)
    #pprint.pprint(itemDict[u'treeDb'])
    l = localItem.localJsonItem('3fe6382b-0219-40c7-add3-2f3b60aeb368', itemDict['workingDir'], itemDict[u'treeDb'], itemDict['legacyFilePath'])
    

    try:
        s = objSync.objUpdater()
        #print '-----------------'
        #s.updateChildren(g, l)
        s.updateChildren(l, g)
        
    except IOError:
        print 'exception occurs'
        pass
    settings['otherSettings'] = itemDict
    c.save(settings)
        
