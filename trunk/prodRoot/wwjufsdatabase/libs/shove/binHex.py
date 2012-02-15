class nonUnicode: pass

class binHex:
    def en(self, s):
        if type(s) != unicode:
            raise nonUnicode
        res = u''
        #print type(s)
        for i in s:
            #print i
            #print type(i)
            res += u"%04X"%ord(i)
            #print res
        #print res
        return res
    def de(self, s):
        if type(s) != unicode:
            raise nonUnicode
        res = ''
        flag = 0
        left = ''
        for i in s:
            if 3 == flag:
                left +=i
                #print 'adding:',left
                res += unichr(int(left, 16))
                flag = 0
                left = ''
                #print res
            else:
                left += i
                flag += 1
        #print unicode(res)
        return res
