
def login():
    import libs.services.services
    s = libs.services.services.services()
    q = s.getQuery()
    h = s.getHtmlGen()

    h.genHead()

    if (s.getDefaultGuestUser() == s.getUser()) or (s.getUser() is None):
        p = [['t',s.getDefaultLoginUsernameParamName()],
            ['t',s.getDefaultLoginPasswordParamName()]]
        if q.has_key('nextUrl'):
            p.append(['h','nextUrl',q['nextUrl'][0]])
        h.genForm('/apps/user/login.py',p)
    else:
        h.write('hello %s'%s.getUser())
        #h.redirect(q['nextUrl'][0])
        

    h.write('<a href="/apps/tree/showJsNamedTree.py">/apps/tree/showJsNamedTree</a><br/>')
    if q.has_key('nextUrl'):
        h.write('<a href="%s">%s</a><br/>'%(q['nextUrl'][0],q['nextUrl'][0]))

    h.genEnd()
        
login()