import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
        
def getThumb(path, targetDir):
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
            newPath = picThumbGenerator.genPicThumb(path, targetDir)
        except picThumbGenerator.pictureFormatNotSupported:
            try:#if True:
                    newPath = ffmpegThumb.genVideoThumb(path, targetDir)
                    #return "complete transform"
                    #return newPath
            except:
                pass
    return newPath