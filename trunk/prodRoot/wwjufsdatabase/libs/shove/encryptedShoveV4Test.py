# -*- coding: gb2312 -*-
from encryptedShoveV4 import *
if __name__ == "__main__":
    s = Shove('d:/tmp/testing.sqliteShoveDb')
    s[u'hello'] = u'good'
    s[u'my'] = u'ok'
    print s[u'hello']
    s[u"你好"] = [u"再见",u"走了"]
    print s[u"你好"]
    print u','.join(s[u"你好"])
    #print s['G:/app/wwj/hello/06-45166.jpg']
