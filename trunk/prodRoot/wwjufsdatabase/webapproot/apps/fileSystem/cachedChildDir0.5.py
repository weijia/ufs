import libSys
import libs.ufs.ufsTreeItem as ufsTreeItem
import desktopApp.lib.localTreeItem as localTreeItem


def jsIdEncoding(s):
    '''
    This function is used to encode the item id of jstree as jstree can not manipulate id with ":" correctly
    '''
    l = s.split(u"_", 1)
    if len(l[0]) == 1:
        s = u":".join(l)
    return s


class MainPage(webapp.RequestHandler):
    def get(self):
        path = self.request.get("path")#already changed to unicode
        path = jsIdEncoding(path)
        try:
            p = ufsTreeItem.getUfsTreeItem(path)
        except ValueError:
            #No schema/protocol string. Normal dir
            p = localTreeItem.localTreeItem(path)
