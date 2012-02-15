import libs.http.queryParam
import libs.services.servicesV2 as service


def getUnicodeParam(queryInfo):
    '''
    All quoted string will be decoded automatically, so if the decoding is not required, please be careful
    '''
    return queryInfo.getAllFieldStorageUnicode()

def getRequestedParam(queryParam, paramDefaultDict):
    #queryParam's every element should be a list
    res = {}
    for i in paramDefaultDict:
        if paramDefaultDict[i] is None:
            #ParamRequired
            if len(queryParam[i]) == 1:
                res[i] = queryParam[i][0]
            else:
                res[i] = queryParam[i]
        else:
            #Param has a default value if it does not exist in queryParam
            if queryParam.has_key(i):
                if len(queryParam[i]) == 1:
                    res[i] = queryParam[i][0]
                else:
                    res[i] = queryParam[i]
            else:
                #No value in queryParam, use the default
                res[i] = paramDefaultDict[i]
    return res

def paramWithDefault(paramDefaultDict, queryInfo):
    return getRequestedParam(getUnicodeParam(queryInfo), paramDefaultDict)