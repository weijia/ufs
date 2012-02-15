# -*- coding: gb2312 -*- 
from binHex import *
        
if __name__ == "__main__":
    b = binHex()
    #print b.en(u"good")
    #print b.de(b.en(u"good"))
    print b.en(u"你好")
    print b.de(b.en(u"你好"))