import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
import configDict as configDict

'''
class configInterface(UserDict.DictMixin):
    def __init__(self, defaultDict, configPath):
        pass
    def store(self, configPath):
        pass
    def __getitem__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
'''
        
class configFileDict(configDict.configInterface):
    def __init__(self, configPath, defaultDict = {}):
        if os.path.isfile(configPath):
            raise 'config file dict can only be created with file.'
        self.configPath = configPath
        floatFilenames = []
        filenameDict = 
        for i in os.listdir(self.configPath):
            floatFilenames[float(i)] = i
        
        '''
        try:
            f = open(self.configPath,'r')
            self.config = json.load(f)
            f.close()
        except IOError:
            self.config = defaultDict
        '''
    def store(self):
        s = json.dumps(self.config, sort_keys=True, indent=4)
        f = open(self.configPath,'w')
        f.write(s)
        f.close()

    def __getitem__(self, key):
        return self.config[key]
    def __setitem__(self, key, value):
        self.config[key] = value
    def __delitem__(self, key):
        del self.config[key]
