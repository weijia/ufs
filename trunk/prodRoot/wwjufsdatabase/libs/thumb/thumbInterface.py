import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
        
def getThumb(path, targetDir):
    newPath = None
    ext = path.split('.')[-1].lower()
    if ext in ['exe']:
        try:
            newPath = appThumb.genAppThumb(path, targetDir)
        except:
            return None
    else:
        try:
            newPath = picThumbGenerator.genPicThumb(path, targetDir)
        except picThumbGenerator.pictureFormatNotSupported:
            try:#if True:
                    newPath = ffmpegThumb.genVideoThumb(path, targetDir)
                    #return "complete transform"
                    #return newPath
            except:
                pass
    return newPath