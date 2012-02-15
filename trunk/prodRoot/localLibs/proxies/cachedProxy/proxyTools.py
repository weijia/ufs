import mimetypes

typeExtMapping = {'application/rss+xml': 'xml'}

def getExtentionFromContentType(value):
  filenameExt = '.txt'
  exts = mimetypes.guess_all_extensions(value.split(';')[0])
  try:
    filenameExt = exts[0]
  except IndexError:
    types = value.split(';')
    try:
      filenameExt = typeExtMapping[types[0]]
    except KeyError:
      print 'unknown type, %s'%(value)
      filenameExt = '.xml'
  return filenameExt

def genExtFromHeaders(lowcaseHeadersDict):
  filenameExt = '.txt'
  filenameEncoding= ''
  if lowcaseHeadersDict.has_key('content-type'):
    filenameExt = getExtentionFromContentType(lowcaseHeadersDict['content-type'])
  if lowcaseHeadersDict.has_key('content-encoding'):
    filenameEncoding = '.gz'
  return filenameExt+filenameEncoding