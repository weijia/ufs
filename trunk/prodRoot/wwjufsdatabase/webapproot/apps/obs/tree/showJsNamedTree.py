import libs.services.services
import libs.tree.showJsNamedTreeHtml



def genTree():
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.logS('before head')
    h.genHead('file tree')
    #h.setTitle('file tree')
    h.logS('after head')
    user = s.getUserAutoRedirect('/apps/test/showJsNamedTree.py')
    h.write('<body>')
    libs.tree.showJsNamedTreeHtml.genTreeInBody(s)
    if user is None:
        h.genEnd()
        return
    h.genEnd()
    
    
    
genTree()