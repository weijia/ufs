'''
Created on 2011-9-30

@author: Richard
'''

import libSys
import libs.collection.objCollection as objCollection


def getCollection(collectionId, objDbInst):
    return objCollection.objCollection(collectionId, objDbInst)

class collectionManager:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
    def getCollection(self, collectionId, objDbInst):
        return objCollection.objCollection(collectionId, objDbInst)
        