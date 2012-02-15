
'''
def replaceAll(exclude, s):
  for i in exclude:
    s = s.replace(i, '_')
  return s
'''
import md5
import os

class urlCache:
  def __init__(self):
    pass
  def isInCache(self):
    return False
  def getUrl(self, url, data = None):
    '''
    If data is None, this function will try to retreive the url page.
    '''
    if data is None:
      #TODO
      raise 'not implemented yet'
      import os
      c = os.getcwd()#For python built in server, it will be server path
      url2dir(url, c)
    else:
      pass
  def getLocalpathForUrlList(self, urlList):
    l = ''
    for i in urlList:
      l += i
    fn = md5.new(l).hexdigest()
    #print 'url:%s, fn:%s'%(l,fn)
    return fn
    
  def cache(self, urlList, data):
    f = open(self.getLocalpathForUrlList(urlList),'w')
    f.write(data)
    f.close()
    
  def getUrlList(self, urlList):
    data = self.getUrlListFromCache(urlList)
    if data is None:
      print 'no cache'
      return self.browseUrlList(urlList)
    else:
      return data
  def getUrlListFromCache(self, urlList):
    data = {}
    curUrlList = []
    for i in urlList:
      curUrlList.append(i)
      fn = self.getLocalpathForUrlList(curUrlList)
      if os.path.exists(fn):
        f = open(fn)
        print 'get cache:', i,fn
        data[i] = f.read()
        f.close()
      else:
        return None
    return data
  def browseUrlList(self, urlList, proxies = {}):
    browseData = {}
    from mechanize import Browser
    br = Browser()
    # Explicitly configure proxies (Browser will attempt to set good defaults).
    br.set_proxies(proxies)
    curUrlList = []
    for i in urlList:
      print 'connecting:',i
      response = br.open(i)
      browseData[i] = response.read()
      #Check cache first.
      curUrlList.append(i)
      self.cache(curUrlList, browseData[i])
    return browseData
