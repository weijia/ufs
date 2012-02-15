import servicesV2

class req:
    def __init__(self):
        self.service = services.services()
        self.html = self.service.getHtmlGen()
    def getUser(self):
        return service.getUser()
    def getParam(self):
        return self.service.getQuery()
    def isLogin(self):
        try:
            self.service.getUser()
            return True
        except:
            return False
    def write(self, s):
        self.html.write(s)
            
    #Do not use the functions below!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def getQueryInfo(self):
        return self.service.queryInfo()