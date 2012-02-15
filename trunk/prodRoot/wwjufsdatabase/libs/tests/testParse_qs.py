transaction = ['add?id=abc&key=def&value=ghi&createapp=zzz/yyy',
'add?id=123&key=456&value=789&createapp=mmm/mmm']

import urlparse

import cgi
print cgi.parse_qs(transaction[0])