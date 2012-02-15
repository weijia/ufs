import sys
import os
import simplejson as json

class cfg:
    def __init__(self, filename = 'config.txt', directory =None):
        if directory is None:
            p = os.path.dirname(sys.argv[0])
        else:
            p = directory
        self.fullP = os.path.join(p, filename)
        print 'reading:',self.fullP
        try:
            f = open(self.fullP,'r')
            self.settings = json.load(f)
            f.close()
        except IOError:
            self.settings = {}

    def getSettings(self):
        return self.settings
        
    def save(self, settings):
        f = open(self.fullP,'wt')
        json.dump(settings,f)
        f.close()