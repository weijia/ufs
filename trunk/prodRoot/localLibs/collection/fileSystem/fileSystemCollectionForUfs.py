import localLibSys
import wwjufsdatabase.libs.collection.collectionInterface as collectionInterface
import wwjufsdatabase.libs.utils.configurationTools as config
import fileSystemCollection

class fileSystemCollectionForUfs(fileSystemCollection.fileSystemCollection):
    def getUfsUrl(self, localUrl):
        return u"ufsFs"+config.getFsProtocolSeparator()+config.getLocalHostId()+u"/"+localUrl
    def getRange(self, start, cnt):
        res = fileSystemCollection.fileSystemCollection.getRange(self, start, cnt)
        ufsRes = []
        for i in res:
            ufsRes.append(self.getUfsUrl(i))
        return ufsRes

        
        
def main():
    f = fileSystemCollectionForUfs('d:/tmp/')
    print f.getRange(0,None)
    f = fileSystemCollectionForUfs('C:/', True)
    print f.getRange(0,None)
    
if __name__=='__main__':
    main()