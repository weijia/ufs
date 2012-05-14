import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
import localLibSys
from wwjufsdatabase.libs.utils.transform import transformDirToInternal
import wwjufsdatabase.libs.utils.objTools as objTools

def internal_get_thumb(path, targetDir, mime_type = None):
    '''
    path: Full Path. The path of the file whose thumbnail will be generated
    targetDir: Directory Path. The target directory where the generated thumbnail will be put in.
    Return: the thumbnail fullPath
    '''
    newPath = None
    ext = path.split('.')[-1].lower()
    if ext in ['exe']:
        try:
            newPath = appThumb.genAppThumb(path, targetDir)
        except:
            return None
    else:
        try:
            newPath = picThumbGenerator.genPicThumb(path, targetDir, mime_type)
        except picThumbGenerator.pictureFormatNotSupported:
            try:#if True:
                    newPath = ffmpegThumb.genVideoThumb(path, targetDir)
                    #return "complete transform"
                    #return newPath
            except:
                pass
    if newPath is None:
        return None
    return transformDirToInternal(newPath)


def getThumb(path, targetDir, mime_type = None, req = None):
    if req is None:
        return internal_get_thumb(path, targetDir, mime_type)
    else:
        #We can have a database from the req. So save the thumb info.
        db = req.getDbSys().getDb("path_to_thumb_db")
        reverse_db = req.getDbSys().getDb("thumb_to_path_db")
        res = internal_get_thumb(path, targetDir, mime_type)
        if not (res is None):
            src_url = objTools.getUfsUrlForPath(path)
            thumb_url = objTools.getUfsUrlForPath(res)
            db[src_url] = thumb_url
            reverse_db[thumb_url] = src_url
        return res
            