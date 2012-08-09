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
from PyQt4.QtGui import QStandardItemModel, QStandardItem
from PyQt4.QtCore import  Qt
class ApplicationList(QtGui.QWidget):
    def __init__(self):
        super(ApplicationList, self).__init__()
        self.ui = uic.loadUi('app_list.ui', self)
        self.model = QStandardItemModel()
        item = QStandardItem('Hello world')
        #item.setCheckState(Qt.Checked)
        #item.setCheckable(True)
        self.model.appendRow(item)
        self.model.appendRow(item)
        self.listView.setModel(self.model)
        self.connect(self.listView.selectionModel(),  
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),  
                     self.store_current_selection) 
        self.show()

    #---------------------------------------------------------------------------
    def store_current_selection(self, newSelection, oldSelection):
        print "changed"
        
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

    
from PyQt4 import QtCore, QtGui, uic

    
class ConsoleManager(UserDict.DictMixin):
    def __init__(self):
        self.app_list = ApplicationList()
        #self.app_list.show()
    def show_app_list(self):
        self.app_list.show()
        
    def __setitem__(self, key, value):
        item = QStandardItem(key)
        self.model.appendRow()
        self.actionDict[key] = value


def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    trayIcon = List2SystemTray(QtGui.QIcon("gf-16x16.png"), w)
    console_man =  ConsoleManager()
    trayIcon["Applications"] = console_man.show_app_list
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()