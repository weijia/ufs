import localLibSys
import wwjufsdatabase.libs.tree.treeSubmissionPackager as treePack
import wwjufsdatabase.libs.collection.collectionSubmissionPackager as collectionPack
import wwjufsdatabase.libs.utils.simplejson as json
import localLibs.collection.fileSystem.localPathSubmitter as submitter
import localLibs.test.testDbSys as testDbSys
    
    
def main():
    d = testDbSys.testDbSys()
    res = submitter.packagePathRecurse("d:/tmp", d)
    s = json.dumps(res, sort_keys=True, indent=4)
    jsonRes = u'\n'.join([l.rstrip() for l in  s.splitlines()])
    print jsonRes
    f = open("d:/tmp/dirJson.json", "w")
    f.write(jsonRes)
    f.close()
    r = json.loads(jsonRes)
    print r
    
if __name__=='__main__':
    main()