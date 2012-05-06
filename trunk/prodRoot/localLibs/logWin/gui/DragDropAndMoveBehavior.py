#import pygtk
#pygtk.require('2.0')
#import gtk
#import gtkTaskbarIconForConsole
#import gtkTxtWndMod
#import logWnd
#import localLibSys
#import localLibs.logSys.logDir as logDir
import gtkDropTarget
import gtkDragMove
#import fileTools
#import beanstalkc
import traceback

#from localLibs.services.beanstalkdServices.beanstalkServiceBaseV2 import gBeanstalkdServerHost, gBeanstalkdServerPort

class DragDropAndMoveBehavior(gtkDropTarget.dropTarget, gtkDragMove.dragMove):
    '''
    This class will generate the floating element and the task bar icon.
    '''
    def __init__(self, parent):
        gtkDragMove.dragMove.__init__(self)
        #gtkDropTarget.dropTarget.__init__(self)
        self.parent = parent

        
    def dropped(self, wid, context, x, y, data, info, time):
        try:
            self.parent.on_dropped()
        except Exception,e:
            traceback.print_exc()
        context.finish(True, False, time)

