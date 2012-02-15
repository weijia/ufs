import time

#-------------------------------------------------------------------------------
picasaFullUrlAttr = 'sys_fullUrl'
mailboxListUuid = 'a4b9cac0-8f16-4210-9310-397f55b6aa8f'
ufsRootUuid = '7904a40c-cd8b-4cd9-9ce2-7c59542331fd'
mailboxListAttr = 'sys_mailboxList'
mailboxAttr = 'sys_mailbox'
mailurlAttr = 'sys_url'
mailFullUrlAttr = 'sys_fullUrl'
userAttr = 'sys_user'
onlineThumbAttr = 'sys_onlineThumb'
passwdAttr = 'sys_passwd'
sysSendStartTimeAttr = 'sys_sendStart'
sysSendEndTimeAttr = 'sys_sendEnd'
sysPicasaFailTimeAttr = 'sys_picasaFailTime'
picasaAccountAttr = 'sys_picasaAccount'
sysDigestAttr = 'sys_md5'
picasaAttr = 'sys_picasaId'
sysTypeAttr = 'sys_type'
picasaObjType = 'picasaAccount'
sysStorageAttr = 'sys_storage'
sysRemoteStorageAttr = 'sys_remoteMailStorage'
sysSentTimeAttr = 'sys_SentTime'
sysMailboxFailTimeAttr = 'sys_mailboxFailTime'
sysSentFromAttr = 'sys_sentFrom'
sysSentToAttr = 'sys_sentTo'
cachedAttr = 'sys_cached'
localPathAttr = 'sys_localPath'
originalPathAttr = 'sys_originalPath'
originalAccessAttr = 'sys_originalAccessTime'
originalChangeAttr = 'sys_originalChangeTime'
originalModifyAttr = 'sys_originalModifyTime'
originalSizeAttr = 'sys_originalSize'
sysDigestAttr = 'sys_md5'
sysTagsAttr = 'sys_tags'
thumbAttr = 'sys_thumb'
encryptedCachedAttr = 'sys_encrypted'
sysLastAccessAttr = 'sys_lastAccess'
sysPicasaAlbumState = 'sys_picasaAlbumState'
sysPicasaAlbumAttr = 'sys_picasaAlbum'
originalParentPathAttr = 'sys_originalParentPath'
dupObjIdAttr = 'sys_dupObjId'
sys_spreadsheetTabIndexAttr = 'sys_spreadsheetTabIndex'
sys_spreadsheetRowAttr = 'sys_spreadsheetRow'
sys_spreadsheetColAttr = 'sys_spreadsheetCol'
sys_templateIdAttr = 'sys_templateId'
sys_cellPosIdAttr = 'sys_cellPosId'
sys_cellValueAttr = 'sys_cellValue'
sys_cellValueIdAttr = 'sys_cellValueId'
sys_cellTemplateValueIdAttr = 'sys_cellTemplateValueId'
sys_sampleSheetUuidAttr = 'sys_sampleSheetUuid'
sys_spreadsheetTabNameAttr = 'sys_spreadsheetTabName'
applicationStopAttr = 'sys_appStop'
sys_childItemList = 'sys_childItemList'
#-------------------------------------------------------------------------------



objectIdTypeList = ['sys_onlineThumb', picasaAttr, 'sys_cached',
    'sys_thumb','sys_picasaAccount','sys_storage','sys_remoteMailStorage',
    'sys_sentTo','sys_sentFrom','sys_mailboxList','sys_mailbox','sys_objId',
    'sys_ffImgDownLogFile', 'sys_ffImgDownFileId','sys_dupObjId',sys_sampleSheetUuidAttr,
    sys_cellTemplateValueIdAttr,sys_cellValueIdAttr,sys_templateIdAttr, sys_cellPosIdAttr, 'sys_cellPos']
timeTypeList = ['sys_originalChangeTime','sys_originalAccessTime',
    'sys_originalModifyTime','sys_lastAccess','sys_sendStart','sys_sendEnd',
    'sys_SentTime','sys_mailboxFailTime',	'sys_ffImgDownDate']
urlTypeList = ['sys_ffImgDownOriginalUrl','sys_ffImgDownFileMissedUrl']
#Can not browser the local path within web page
localPathTypeList = ['sys_originalPath', 'sys_localpath']

def addShowObjAttr(objId):
    return '<a href=showObjAttr.py?objectId=%s>%s</a>'%(objId,objId)


def showOriginal(data):
    return data

def showTime(data):
    return time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime(float(data)))

def showLocalPath(data):
    return '<a href=file:///%s>%s</a>'%(data,data)

def showUrl(data):
    return '<a href=%s>%s</a>'%(data,data)

class commonAttrSys:
    def __init__(self):
        self.attrFuncMapping = {}
        self.attrFuncMapping[addShowObjAttr] = objectIdTypeList
        self.attrFuncMapping[showTime] = timeTypeList
        self.attrFuncMapping[showUrl] = urlTypeList
        #self.attrFuncMapping[showLocalPath] = localPathTypeList

    def getAttrOutput(self, attrName):
        for i in self.attrFuncMapping.keys():
            if type(self.attrFuncMapping[i]) == list:
              try:
                  self.attrFuncMapping[i].index(attrName)
                  return i
              except ValueError:
                  pass
            else:
                if self.attrFuncMapping[i] == attrName:
                    return i
        return showOriginal

