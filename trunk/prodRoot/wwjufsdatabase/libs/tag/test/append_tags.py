'''
Created on 2012-4-19

@author: Richard
'''

import wwjufsdatabase.libs.tag.tagSystemInterfaceV2 as tagSystem
if __name__ == '__main__':
    import wwjufsdatabase.libs.services.servicesV2 as service
    req = service.req()
    t = tagSystem.getTagSysObj(req.getDbSys())
    #e = t.tag(u"C:/", u"test")
    t.removeTag(u"C:/", u"test")