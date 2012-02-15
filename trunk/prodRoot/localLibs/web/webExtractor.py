from lxml.html.soupparser import fromstring
from lxml import etree

def getXpath(root, t):
  #Find the element with text: t
  d = root.xpath("//td[contains(text(), '%s')]"%t)
  tree = etree.ElementTree(root)
  #Get the xpath
  for i in d:
    p = tree.getpath(i)
    #print p, t
    #print root.xpath(p.replace('/html/',''))[0]
    return p
  return None

def getElementFromTemplateInHtml(html, knownHtml, knownTextDict):
  res = {}
  for i in knownTextDict.keys():
    #print i
    #print 'finding:',knownTextDict[i]
    res[i] = getElementFromTemplateInHtmlElem(fromstring(html), fromstring(knownHtml), knownTextDict[i])
  return res
    
def getElementFromTemplateInHtmlElem(htmlElemRoot, knownHtmlElemRoot, knownText):
  e = getXpath(knownHtmlElemRoot, knownText)
  if e is None:
    print '\ncan not find:',knownText,'\n\n\n'
    raise ''
  xp = e.replace('/html/','')
  #print xp
  #print htmlElemRoot.xpath(xp)
  #print 'found:',htmlElemRoot.xpath(xp)[0].text
  return htmlElemRoot.xpath(xp)[0].text

def main(argv=None):
    if argv is None:
      argv = sys.argv
      #print argv
    if len(argv) < 2:
        pass
    f1 = open('50dbb0570e45771ca4d7c2204cd2649f')
    f2 = open('38d54af2d8f7d8628acfae40933675a1')
    d1 = f1.read()
    d2= f2.read()
    print getElementFromTemplateInHtmlElem(fromstring(d2),fromstring(d1),'Alarms are wrongly mapped or reported in BTS when using CTU2D')
    print getElementFromTemplateInHtml(d2, d1,{'res':'Alarms are wrongly mapped or reported in BTS when using CTU2D'})

import sys
if __name__ == "__main__":
  sys.exit(main())