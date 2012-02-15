import beanstalkc
import urllib2
import os

import fileTools
import misc

def dl_img(url, target):
    re = urllib2.Request(url)  
    rs = urllib2.urlopen(re).read()
    open(target, 'wb').write(rs)


def img_dl():
    beanstalk = beanstalkc.Connection(host='localhost', port=11300)
    beanstalk.use('img_dl')
    beanstalk.watch('img_dl')
    beanstalk.ignore('default')
    img_root = os.path.join(os.getcwd(), "img")
    poster = beanstalkc.Connection(host='localhost', port=11300)
    poster.use('img_poster')
    misc.ensureDir(img_root)
    while True:
        job = beanstalk.reserve()
        print "got job", job.body
        url = job.body
        target = fileTools.getTimestampWithFreeName(img_root, '')
        dl_img(url, target)
        print target+";"+url
        poster.put(str(target+";"+url))
        job.delete()


if __name__ == "__main__":
    img_dl()