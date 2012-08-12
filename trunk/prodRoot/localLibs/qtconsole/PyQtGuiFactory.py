from PyQtConsoleOutputWnd import PyQtConsoleOutputWnd
import PyQt4.QtGui as QtGui
import sys
from TaskbarIcon import List2SystemTray
from PyQt4 import QtCore
import fileTools

class GuiFactoryBase(object):
    def __init__(self):
        pass
        
    def create_taskbar_icon_app(self):
        pass
        
    def create_console_output_wnd(self, parent, logFilePath = None):
        pass
    def start_msg_loop(self):
        pass
    def get_app_list(self):
        pass
        
class PyQtGuiFactory(GuiFactoryBase):
    def __init__(self):
        super(PyQtGuiFactory, self).__init__()
        self.app = QtGui.QApplication(sys.argv)
        
    def create_taskbar_icon_app(self):
        self.w = QtGui.QWidget()
        icon_full_path = fileTools.findFileInProduct("gf-16x16.png")
        self.trayIcon = List2SystemTray(QtGui.QIcon(icon_full_path), self.w)
        #self.trayIcon["Example"] = exampleAction
        return self.trayIcon
        
    def create_console_output_wnd(self, parent, logFilePath = None):
        return PyQtConsoleOutputWnd(parent, logFilePath)
        
    def start_msg_loop(self):
        sys.exit(self.app.exec_())
    def timeout(self, milliseconds, callback):
        self.ctimer = QtCore.QTimer()
        # constant timer
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), callback)
        self.ctimer.start(milliseconds)
    def exit(self):
        QtGui.QApplication.quit()
