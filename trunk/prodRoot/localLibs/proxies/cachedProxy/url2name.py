import os
import string
import binascii
ARCHIVE_MAXIMUM_FILE_SIZE = 50
SYS_MAXIMUM_FILE_SIZE = 250

def log(a='',b='',c='',d='',v=''):
  print a,b,c,d,v
from md5 import md5

ARCHIVE_FILE_NAMES = 'plain'

def url2dir(url, base = 'd:\\cache'):
  '''
  For each part in the url, if it exeed the ARCHIVE_MAXIMUM_FILE_SIZE, change it
  to hash.
  If the total len of the generated dir is bigger than sys can accept (
  >SYS_MAXIMUM_FILE_SIZE). Change the last part of the part to an hash
  that is from the url.
  '''
  dirname = url
  dirname = string.replace(dirname, '://', os.sep, 1)
  dirname = string.replace(dirname, '/', os.sep)
  if dirname[-1:] == os.sep:
    dirname += 'index'

  if os.name == 'dos' or os.name == 'nt':
    for c in [':', '*', '?', '"', '<', '>', '|']:
      dirname = string.replace(dirname, c, '%'+string.upper(binascii.b2a_hex(c)))
  copyOfDirname = dirname
  dirname2 = string.split(dirname, os.sep)
  for i in range(len(dirname2)):
    #print dirname2[i]
    if len(dirname2[i]) > ARCHIVE_MAXIMUM_FILE_SIZE:
      #print 'one exceeds max'
      dirname2[i] = md5(dirname2[i]).hexdigest()

  dirname = string.join(dirname2, os.sep)      
  dirname = os.path.join(base, dirname)

  if len(dirname) > SYS_MAXIMUM_FILE_SIZE:
    h = md5(copyOfDirname).hexdigest()
    dirname = os.path.join(base, copyOfDirname)
    dirname = dirname[0:SYS_MAXIMUM_FILE_SIZE - len(h)]+h
    #print '------------------------------------generated dir name is',dirname
    #print 'url is:',copyOfDirname
  else:
    #print '-----------------gen dir', dirname
    pass
  # Find a unique name in case of collisions:
  if not os.path.isdir(dirname):
    while os.path.exists(dirname) and not os.path.isdir(dirname):
      dirname += '_'

    os.makedirs(dirname)
    #log('Making directory: '+dirname+'\n', v=2)
  return dirname


def main():
  print url2dir('http://www.ruby-doc.org/stdlib/libdoc/xmlrpc/rdoc/index.html')
  print url2dir('http://img127.cocoimage.com/img.php?id=1240583982&q=&jump=4356069981&ru=aHR0cDovL2ltZzEyNy5jb2NvaW1hZ2UuY29tL2ltZy5waHA%2FaWQ9MTI0MDU4Mzk4Mg%3D%3D')
  print url2dir('http://www.ruby-doc.org/stdlib/libdoc/xmlrpc/rdoc/index.html')


if __name__ == "__main__":
    main()
