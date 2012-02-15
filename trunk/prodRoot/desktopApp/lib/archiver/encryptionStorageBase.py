import archiver as archiver
import libSys
#import localLibs.localLibs
import wwjufsdatabase.libs.utils.transform as transform
import wwjufsdatabase.libs.utils.misc as misc
import localLibs.collection.fileSystem.fileSystemCollection as fsCollection
import shutil
import os
#from stat import *
#import wwjufsdatabase.libs.utils.simplejson as json
import archiveStorageBase as archiveStorageBase

#import wwjufsdatabase.libs.encryption.arc4Encryptor as arc4Enc

from Crypto.Cipher import ARC4 as cipher
import desktopApp.lib.encryption.aesFileEncryptor as enc

class arc4EncSimpleCopier:
    def __init__(self, key):
        self.key = key
    def copy(self, src, dest):
        keyobj = cipher.new(self.key)
        inF = open(src, 'rb')
        oF = open(dest, 'wb')
        oF.write(keyobj.encrypt(inF.read()))
        inF.close()
        oF.close()
        
class arc4DecSimpleCopier:
    def __init__(self, key):
        self.key = key
    def copy(self, src, dest):
        keyobj = cipher.new(self.key)
        inF = open(src, 'rb')
        oF = open(dest, 'wb')
        oF.write(keyobj.decrypt(inF.read()))
        inF.close()
        oF.close()

class aesEncSimpleCopier:
    def __init__(self, key):
        self.key = key
    def copy(self, src, dest):
        enc.encrypt_file(self.key, src, dest)
        
class aesDecSimpleCopier:
    def __init__(self, key):
        self.key = key
    def copy(self, src, dest):
        enc.decrypt_file(self.key, src, dest)
        
        
        
class encryptionStorageBase(archiveStorageBase.plainArchiveStorage):
    def __init__(self, srcRoot, storageRoot, stateStoragePath = 'd:/state.txt', 
            encCopier = arc4EncSimpleCopier('defaultPass')):
        #print srcRoot
        self.encCopier = encCopier
        archiveStorageBase.plainArchiveStorage.__init__(self, srcRoot, storageRoot, 
            stateStoragePath)

    def store(self, element):
        #print 'storing....'
        relPath = element.getAbsPath().replace(self.srcRoot+'/', '')
        targetPath = transform.transformDirToInternal(os.path.join(self.storageRoot, relPath))
        #dirPath = os.path.dirname(targetPath)
        try:
            targetSaved = self.config[targetPath]
        except KeyError:
            targetSaved = None
        if targetSaved != os.stat(element.getAbsPath()).st_mtime:
            #if not os.path.exists(targetPath):
            print 'copying "%s" to "%s"'%(relPath, targetPath)
            self.encCopier.copy(element.getAbsPath(), targetPath)
        else:
            print 'file exists, skip:', targetPath
            #print targetSaved, os.stat(element.getAbsPath()).st_mtime

if __name__ == "__main__":
    #flag = True
    flag = False
    if flag:
        src = archiveStorageBase.folder('d:/tmp/test')
    else:
        src = archiveStorageBase.folder('d:/tmp/target')
    ar = archiver.archiverInterface()
    if flag:
        s = encryptionStorageBase('d:/tmp/test', 'd:/tmp/target', encCopier = arc4EncSimpleCopier('defaultPass'))
    else:
        s = encryptionStorageBase('d:/tmp/target', 'd:/tmp/targetNoEnc', encCopier = arc4DecSimpleCopier('defaultPass'))
    ar.archive(src, s)
    s.saveState()   
    