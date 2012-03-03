#http://blog.donews.com/limodou/archive/2005/11/13/625145.aspx
import zipfile
import os.path
import os

gLocalEncode = 'gbk'

def encode2Local(s):
    if type(s) == unicode:
        return s.encode(gLocalEncode)
    else:
        return s

def decode2Local(s):
    return s.decode(gLocalEncode)
        
        
class ZFile(object):
    def __init__(self, filename, mode='r', basedir=''):
        self.filename = filename
        self.mode = mode
        if self.mode in ('w', 'a'):
            self.zfile = zipfile.ZipFile(filename, self.mode, compression=zipfile.ZIP_DEFLATED)
        else:
            self.zfile = zipfile.ZipFile(filename, self.mode)
        self.basedir = basedir
        if not self.basedir:
            self.basedir = os.path.dirname(filename)
        
    def addfile(self, path, arcname=None):
        '''
        if (type(path) != unicode):
            raise 'input must be unicode'
        if (not (arcname is None)):
            if (type(arcname) != unicode):
                raise 'input must be unicode'
        '''
        path = path.replace('\\', '/')
        if not arcname:
            if path.startswith(self.basedir):
                arcname = path[len(self.basedir):]
            else:
                arcname = ''
        #########################
        # The first param should be unicode, so zipfile can retrieve the info from
        # file system by this path, check zipfile line 541
        #self.zfile.write(encode2Local(path), encode2Local(arcname))
        self.zfile.write(encode2Local(path), encode2Local(arcname))
        #return the info of the newly added file
        return self.zfile.filelist[-1]
            
    def addfiles(self, paths):
        for path in paths:
            if isinstance(path, tuple):
                self.addfile(*path)
            else:
                self.addfile(path)
            
    def close(self):
        self.zfile.close()
        
    def extract_to(self, path):
        for p in self.zfile.namelist():
            self.extract(p, path)
            
    def extract(self, filename, path):
        '''
        Extract filename to path. Target  file would be path/filename
        '''
        if not filename.endswith('/'):
            f = os.path.join(path, filename)
            dir = os.path.dirname(f)
            if not os.path.exists(dir):
                os.makedirs(dir)
            #print 'extracting:', f
            zipFilename = encode2Local(filename)
            file(f, 'wb').write(self.zfile.read(zipFilename))
            return f
        
        raise "Invalid filename"
    def list(self):
        for i in self.zfile.namelist():
            yield decode2Local(i)
        
def create(zfile, files):
    z = ZFile(zfile, 'w')
    z.addfiles(files)
    z.close()
    
def extract(zfile, path):
    z = ZFile(zfile)
    z.extract_to(path)
    z.close()