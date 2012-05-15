import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
import localLibSys
from wwjufsdatabase.libs.utils.transform import transformDirToInternal
from wwjufsdatabase.libs.utils.objTools import getUfsUrlForPath


g_non_video_file_ext_list = ["zip", "dll", "cab", "txt", "iso", "rar", "pdf", 
                             "doc", "docx", "xls", "xlsx", "7z", "apk", "log",
                             "sis", "sisx", "asp", "aspx", "py", "pyc", "java",
                             "class", "php", "c", "cpp", "h", "hpp", "egg", "tar",
                             "gz", "img", "msi", "jar", "xpi", "crx"]


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
            if not (ext in g_non_video_file_ext_list):
                try:#if True:
                        newPath = ffmpegThumb.genVideoThumb(path, targetDir)
                        #return "complete transform"
                        #return newPath
                except:
                    pass
            else:
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
            src_url = getUfsUrlForPath(path)
            thumb_url = getUfsUrlForPath(res)
            db[src_url] = thumb_url
            reverse_db[thumb_url] = src_url
        return res
            