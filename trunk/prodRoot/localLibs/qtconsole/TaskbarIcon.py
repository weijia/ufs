import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exitHandler)
        self.setContextMenu(self.menu)
    def exitHandler(self):
        QApplication.quit()
        
        
import UserDict


class List2SystemTray(UserDict.DictMixin):
    def __init__(self, icon, parent=None):
        self.systemTrayIcon = SystemTrayIcon(icon, parent)
        self.systemTrayIcon.show()
        self.actionDict = {}
        
    def __setitem__(self, key, value):
        action = self.systemTrayIcon.menu.addAction(key)
        action.triggered.connect(value)
        self.actionDict[key] = value
    def __delitem__(self, key):
        action = self.systemTrayIcon.menu.removeAction(key)
        action.triggered.connect(value)
        del self.actionDict[key]

def exampleAction():
    print "Example action triggered"
        
def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    trayIcon = List2SystemTray(QtGui.QIcon("gf-16x16.png"), w)
    trayIcon["Example"] = exampleAction
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()