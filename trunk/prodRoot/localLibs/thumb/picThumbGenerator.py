import os
import re
import wwjufsdatabase.libs.utils.transform as transform

g_default_thumb_size = 256

class pictureFormatNotSupported:
    pass

def getProdRoot():
    c = os.getcwd()
    while c.find('prodRoot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c,'prodRoot')

rootPath = getProdRoot()
os.environ["PATH"] = os.environ["PATH"]+";"+rootPath
import magic
    
def picFormatSupported(ext):
    pat = re.compile("jpe{0,1}g", re.I)
    if pat.search(ext):
        return True
    if re.compile("png", re.I).search(ext):
        return True
    if re.compile("ico", re.I).search(ext):
        return True
    else:
        return False

        
def picFormatSupportedV2(fullPath, mime_type = None):
    if mime_type is None:
        rootPath = getProdRoot()
        magicPath = os.path.join(rootPath, "share\\file\\magic")
        #print 'magic path: ',magicPath
        if not os.path.exists(magicPath):
            raise "Magic file lost"
        #print "magic path is", magicPath
        #os.environ["MAGIC"] = magicPath
        m = magic.Magic(magic_file=magicPath)
        res = m.from_file(fullPath)
    else:
        res = mime_type
    #print res
    if res.find('image') != -1:
        #print 'image', fullPath
        return True
    else:
        print "mime type have no thumb:", res
        return False
        
def genPicThumb(local_path, dest_dir, mime_type = None):
    #If no thumbnail exist, create one
    #print '-----------------------localpath:',local_path
    basename = os.path.basename(local_path)
    #print "basename:" + basename
    
    ext = basename.split(".")[-1]
    #print ext
    #if picFormatSupported(ext):
    if picFormatSupportedV2(local_path, mime_type = None):
        #It is a jpeg file, currently no other type supported
        import Image #Using PIL lib 
        im = Image.open(local_path)
        # convert to thumbnail image
        im.thumbnail((g_default_thumb_size, g_default_thumb_size), Image.ANTIALIAS)
        # don't save if thumbnail already exists
        #Use _T as the thumb file end to indicate the end of the original firl
        thumb_path_without_ext = os.path.join(dest_dir, basename.split(".")[0]+"_T")
        import random
        while os.path.exists(thumb_path_without_ext+".jpg"):
            thumb_path_without_ext += str(random.randint(0,10))
        thumb_path = thumb_path_without_ext+'.jpg'
        #print thumb_path.encode("utf8","replace")
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.save(thumb_path,  "JPEG")
        return transform.transformDirToInternal(thumb_path)
    else:
        print 'non jpeg file not supported'
        raise pictureFormatNotSupported
    

def returnThumbString(local_path):
    import Image #Using PIL lib 
    import cStringIO
    import StringIO
    im = Image.open(local_path)
    # convert to thumbnail image
    im.thumbnail((128, 128), Image.ANTIALIAS)
    f = cStringIO.StringIO()
    im.save(f,  "JPEG")
    return f