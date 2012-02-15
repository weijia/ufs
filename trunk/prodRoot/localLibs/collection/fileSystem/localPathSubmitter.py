import localLibSys
import wwjufsdatabase.libs.tree.treeSubmissionPackager as treePack
import wwjufsdatabase.libs.collection.collectionSubmissionPackager as collectionPack
import wwjufsdatabase.libs.utils.simplejson as json
import os


def packagePath(path, dbSysInst, res):
    treePack.packageTreePath(path, dbSysInst, res)
    collectionPack.packageCollection(path, dbSysInst, res)
    return res



def packagePathRecurse(path, dbSysInst):
    res = {}
    treePack.packageTreePath(path, dbSysInst, res)
    for root, dirs, files in os.walk(unicode(path)):
        for k in dirs:
            collectionPack.packageCollection(os.path.join(root,k), dbSysInst, res)
    return res


