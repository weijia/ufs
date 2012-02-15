



class serverResponseParser:
    def parseAttrValuePairs(self, f):
        '''
        The response would be as following:
        sys_lastAccess:
        1239588949.63
        
        sys_fullUrl:
        googleaccount@gmail.com
        
        sys_passwd:
        passwd
        
        sys_url:
        gmail.com
        
        sys_user:
        myfirstmaildisk
        
        sys_tags:
        abc
        def
        
        The result may be as following:
        result['sys_lastAccess'] = [1239588949.63]
        result['sys_fullUrl'] = [myfirstmaildisk@gmail.com]
        result['sys_tags'] = ['abc','def']
        ...
        '''
        print 'returned value-------------------------------'
        resp = f.read()
        print resp
        result = {}
        l = resp.split('\n')
        resF = False
        keyF = False
        for i in l:
            if resF:
                #Result part
                if not keyF:
                    #This is the key part
                    if i == "":
                        continue
                    keyF = True
                    key = i[0:len(i)-1]
                    print 'find key:%s'%key
                    result[key] = []
                else:
                    #This is the value part
                    if i == "":
                        keyF=False
                        continue
                    print 'find value for key:%s is %s'%(key,i)
                    result[key].append(i.decode('gb2312'))
            if i == '\'\'\'\'----------------':
                resF = True
        if len(result.keys()) == 0:
            return None
        return result
    def parseValueList(self, f):
        '''
        The response would be as following (\' is just '):
        {u'uuid': u'6f3f7099-df07-44a8-8561-857f59978c73', u'key': u'arraykey'}
        \'\'\'\'----------------
        first
        second
        
        The returned values is:
        result = ['first','second']
        '''
        print 'returned value-------------------------------'
        resp = f.read()
        print resp
        result = []
        l = resp.split('\n')
        resF = False
        for i in l:
            if resF:
                #Result part
                if i != "":
                    result.append(i.decode('gb2312'))
            if i == '\'\'\'\'----------------':
                resF = True
        if len(result) == 0:
            return []
        return result
    def parseValuePair(self, f):
        print 'returned value-------------------------------'
        resp = f.read()
        #print resp
        result = []
        l = resp.split('\n')
        resF = False
        for i in l:
            if resF:
                #Result part
                if i != "":
                    id, aUuid = i.split(',')
                    return int(id),aUuid
            if i == '\'\'\'\'----------------':
                resF = True
        return None, None
