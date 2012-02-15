def splitWithChars(s, separatorList):
    '''
    Separate string with multiple chars, such as ",\r\n\t" etc
    '''
    r = [s]
    for i in separatorList:
        t = []
        for j in r:
            t.extend(j.split(i))
        r = t
    return r
    
class specialEncodingError: pass
import re
class nonUnicodeError: pass
'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
If there is a number that following the removing Char will cause problem if the length of the numbers for the escaped char.

For exsample: ":" is the removing char, "\\" is the escapeChar, then ":12" will cause problem. Solution is to use fixed length of number for escaped char.
'''
import sys
def decodeChar(matchobj):
    v = matchobj.group(0)
    print >>sys.stderr, "--------"+matchobj
    return unichr(int(v[1:]))
    
def l(s):
    #print >>sys.stderr, s
    #print s
    pass
    
class specialEncoding:
    def __init__(self, removingChars, escapeChar):
        '''
        All removing chars should be unicode
        '''
        if type(removingChars) != list:
            raise specialEncodingError
        for i in removingChars:
            if type(i) != unicode:
                raise nonUnicodeError
        if type(escapeChar) != unicode:
            raise nonUnicodeError            
        self.removingChars = removingChars
        self.escapeChar = escapeChar
        self.escapeCharNumLen = (len(removingChars)/20)+1
        
    def en(self, s):
        '''
        \\a->\\\\a
        b->\98#b's ascii is 98
        '''
        if type(s) != unicode:
            raise nonUnicodeError
        s = s.replace(self.escapeChar, self.escapeChar+self.escapeChar)
        cnt = 0
        for i in self.removingChars:
            #print s
            s = s.replace(i, self.escapeChar+u'0'*(self.escapeCharNumLen-len(str(cnt)))+unicode(str(cnt)))
            #print 'after replace:%s, %s'%(i, s)
            cnt += 1
        return s
    def de(self, s):
        if type(s) != unicode:
            raise nonUnicodeError
        #s = re.sub("\\[0-9]+", decodeChar, s)
        state = 0#0: normal, 1: one escapeChar received, 2: number received
        r = u""
        num = u""
        for i in s:
            l(u"processing char:"+i)
            if state == 0:
                if i == self.escapeChar:
                    l(u"i is escapeChar")
                    state = 1
                    continue
                else:
                    r += i
                    continue
            if state == 1:
                if i == self.escapeChar:
                    r += self.escapeChar
                    state = 0
                    continue
                else:
                    l("current length:"+str(len(num)))
                    l(u"collecting:"+i)
                    num += i
                    if len(num) == self.escapeCharNumLen:
                        l(u"generating:"+num)
                        r += self.removingChars[int(num)]
                        num = u""
                        state = 0
                
                
        #print >>sys.stderr, s
        #s = s.replace(self.escapeChar+self.escapeChar, self.escapeChar)
        return r
        
#Jquery does not support ":","\"?
#Python 2.7 does not support param with '/'
gEscaping = [u":",u"/"]

'''
def jsIdEncoding(s):
    #####################
    #This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    #
    #return s
    l = s.split(u":", 1)
    if len(l[0]) == 1:
        s = "_".join(l)
    return s

'''

def jsIdEncoding(s):
    '''
    This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    '''
    e = specialEncoding(gEscaping,u"_")
    return e.en(s)

def jsIdDecoding(s):
    e = specialEncoding(gEscaping,u"_")
    #print e.de(s)
    return e.de(s)
    
if __name__ == '__main__':
    v = u"hello\rgoodmorning\thi,,"
    #print 'separating:', v
    print splitWithChars(v, u"\r\t\n,")
    v = u"go\\\\od:ba/d"
    s = specialEncoding([u":",u"/"], u"\\")
    print v
    print s.en(v)
    print s.de(v)
    v = u"D:/"
    s = specialEncoding([u":",u"/"], u"\\")
    print v
    print s.en(v)
    print s.de(v)
    print jsIdDecoding(u"ufsFs\\0//q19420-01/D\\0/")