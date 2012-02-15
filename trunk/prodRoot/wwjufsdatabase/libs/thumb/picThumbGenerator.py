import os
import re
import magic

class pictureFormatNotSupported:
    pass

    
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

        
def picFormatSupportedV2(fullPath):
    magicPath = os.path.join(os.getcwd(), "share\\file\\magic")
    #print "magic path is", magicPath
    #os.environ["MAGIC"] = magicPath
    m = magic.Magic(magic_file=magicPath)
    res = m.from_file(fullPath)
    print res
    if res.find('image') != -1:
        print 'image', fullPath
        return True
    else:
        return False
        
def genPicThumb(local_path, dest_dir):
    #If no thumbnail exist, create one
    #print '-----------------------localpath:',local_path
    basename = os.path.basename(local_path)
    #print "basename:" + basename
    
    ext = basename.split(".")[-1]
    #print ext
    #if picFormatSupported(ext):
    if picFormatSupportedV2(local_path):
      #It is a jpeg file, currently no other type supported
      import Image #Using PIL lib 
      im = Image.open(local_path)
      # convert to thumbnail image
      im.thumbnail((128, 128), Image.ANTIALIAS)
      # don't save if thumbnail already exists
      #Use _T as the thumb file end to indicate the end of the original firl
      thumb_path_without_ext = os.path.join(dest_dir, basename.split(".")[0]+"_T")
      import random
      while os.path.exists(thumb_path_without_ext+".jpg"):
        thumb_path_without_ext += str(random.randint(0,10))
      thumb_path = thumb_path_without_ext+'.jpg'
      print thumb_path.encode("utf8","replace")
      im.save(thumb_path,  "JPEG")
      return thumb_path
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