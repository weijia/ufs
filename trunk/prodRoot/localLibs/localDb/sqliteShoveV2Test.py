# -*- coding: gb2312 -*- 
from sqliteShoveV2 import *
def main():
    s = Shove('d:/tmp/testing.sqliteShoveDb')
    s[u'hello'] = u'good'
    s[u'my'] = u'ok'
    print s[u'hello']
    s[u"���"] = [u"�ټ�",u"����"]
    print s[u"���"]
    print u','.join(s[u"���"])
    #print s['G:/app/wwj/hello/06-45166.jpg']

     
if __name__ == '__main__':
    main()
