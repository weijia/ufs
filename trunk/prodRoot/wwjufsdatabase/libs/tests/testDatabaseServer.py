

transaction = ['id=abc&key=def&value=ghi&createapp=zzz/yyy&action=add',
'id=123&key=456&value=789&createapp=mmm/mmm&action=add']

postcmd = 'http://localhost:9901/apps/database/storage.py'
print postcmd
print '\n'.join(transaction)
import urllib
params = urllib.quote('\n'.join(transaction))
#params = '\n'.join(transaction)
print 'quoted:',params
f = urllib.urlopen(postcmd, params, proxies = None)
print 'returned value-------------------------------'
print f.read()

