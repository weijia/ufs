import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
import localLibSys
from wwjufsdatabase.libs.utils.transform import transformDirToInternal
        
def getThumb(path, targetDir, mime_type = None):
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
            if not (ext in ["zip", "dll", "cab", "txt", "iso", "rar", "pdf", "doc", "docx", "xls", "xlsx"]):
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