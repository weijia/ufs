import libSys
import libs.services.servicesV2 as service
import libs.utils.webUtils as webUtils
import localLibSys
from localLibs.logSys.logSys import *


if __name__=='__main__':
    r = service.req()
    r.resp.genTxtHead()
    param = webUtils.paramWithDefault({"username":None,"passwd":None}, r.getQueryInfo())
    cl(str(param))
    cl("before calling verifyLogin")
    r.verifyLogin()
    u = r.getPrimaryUser()
    cl("primary:"+u.username)
    s = r.getSecondaryUsername()
    sec = []
    for i in s:
        sec.append(i)
    if u.username == param["username"]:
        state = "OK"
    else:
        state = "Wrong"
    r.resp.write(u'{"username":"%s", "secondaryUsers":"%s", "state":"%s"}'%(u.username, u','.join(sec), state))
    r.resp.end()
