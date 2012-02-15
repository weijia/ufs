from optparse import OptionParser
import localLibSys
import desktopApp.lib.archiver.encryptionStorageBase as encryptionStorageBase
import desktopApp.lib.archiver.archiveStorageBase as archiveStorageBase
import desktopApp.lib.archiver.archiverV2 as archiver
import wwjufsdatabase.libs.utils.misc as misc


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-s", "--sourceDir", action="store",help="copy from which directory")
    parser.add_option("-p", "--encryptionPass", action="store",help="encryption password")
    parser.add_option("-t", "--targetDir", action="store", help="target directory")
    parser.add_option("-c", "--configPath", action="store", help="path for the config file")
    (options, args) = parser.parse_args()
        
        
    ar = archiver.archiverInterface()

    src = archiveStorageBase.folder(options.sourceDir)
    misc.ensureDir(options.targetDir)

    s = encryptionStorageBase.encryptionStorageBase(options.sourceDir, options.targetDir,
        stateStoragePath = options.configPath, 
        encCopier = encryptionStorageBase.arc4EncSimpleCopier(options.encryptionPass))
    ar.archive(src, s)
    s.saveState()
