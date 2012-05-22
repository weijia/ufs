#!/usr/bin/env python


#Code from http://hi.baidu.com/pymain/blog/item/f6d62933b81589a25fdf0e12.html
import sys
import random
import string
 
def usage():
    print "Usage: ./randompasswd.py num [num in (1-1024)]"
    exit(1)
 
def randomPassword(num):
    passwd = ''
    seed = string.letters + string.digits
    for i in xrange(num):
        passwd += seed[random.randrange(1,len(seed))]
 
    return passwd
 
def main():
    if len(sys.argv) == 2:
        try:
            num = int(sys.argv[1])
        except:
            usage()
 
        if num in xrange(1,1024):
            print randomPassword(num)
        else:
            usage()
    else:
        print randomPassword(20)
 
if __name__ == '__main__':
    main()