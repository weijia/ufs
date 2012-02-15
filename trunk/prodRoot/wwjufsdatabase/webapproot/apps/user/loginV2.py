import libSys
import libs.services.newService as s

    
def genLogin(req):
    q = req.getParam()#equal to req.getParam()
    if req.isLogin():
        #If not logged in, generate an input place
        p = [['t',''],
            ['t','']]
        if q.has_key('nextUrl'):
            req.append(['h','nextUrl',q['nextUrl'][0]])
        req.genForm('/apps/user/login.py',p)
    else:
        #Already logged in, say hello
        req.write('hello %s'%req.getUser())

    #Write something here?
    
    #Write the next url for user for convenient
    if q.has_key('nextUrl'):
        req.write('<a href="%s">%s</a><br/>'%(q['nextUrl'][0],q['nextUrl'][0]))

    req.genEnd()
        
def main():
    req = s.req()
    genLogin(req)
        
        
if __name__ == '__main__':
    main()