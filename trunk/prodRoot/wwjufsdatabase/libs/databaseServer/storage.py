import sys
import urllib
from valueDbStorage import *



lines = sys.stdin.readlines()
print lines
st = valueDbStorageWrapper()

print '-------------------------unquoted'
for i in lines:
    m = urllib.unquote(i)
    cmd = m.split('\n')
    for li in cmd:
        op, k = li.split('?',1)
        if op == 'add':
            params = k.split('&')
            ret = {}
            for p in params:
                #if the client is a chinese client, and the url is input by hand in url bar,
                #the url will be encoded in 'gb2312'. so it may need encode again
                try:
                #if True:
                    #Change to unicode?
                    ret[urllib.unquote(p.split('=')[0]).decode('gb2312')] = urllib.unquote(p.split('=')[1]).decode('gb2312')
                except:
                #else:
                    ret[urllib.unquote(p.split('=')[0])] = urllib.unquote(p.split('=')[1])
            st.add(ret['uuid'], ret['key'], ret['value'], ret['app'])
        elif op == 'rmKey':
            pa = getParamPairs(k)
            st.rmKey(pa['uuid'], pa['key'], pa['app'])
        elif op == 'rm':
            pa = getParamPairs(k)
            st.rm(pa['uuid'], pa['key'], pa['value'], pa['app'])

st.commit()
