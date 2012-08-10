# -*- coding: utf-8 -*-  
#from QtGui import QTextBrowser
from PyQt4.QtGui import QApplication, QTextBrowser
import sys
    
from PyQt4 import QtGui

class LogOutputWndBase(object):
    def updateView(self, data):
        pass
        
from PyQt4 import QtCore

class QtLogOutputWnd(QTextBrowser):
    update_signel = QtCore.pyqtSignal(object)
    def __init__(self):
        QTextBrowser.__init__(self)
        self.show()
        self.update_signel.connect(self.add_text)
        
    def add_text(self, data):
        self.append(data)
        print data
        
    def updateViewCallback(self, data):
        self.update_signel.emit(data)
        
        
from ConsoleOutputCollector import ConsoleOutputCollector

def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    log_wnd = QtLogOutputWnd()
    runner = ConsoleOutputCollector()
    runner.runConsoleApp(log_wnd, "D:\\codes\\mine\\git\\ufs.git\\trunk\\prodRoot\\", ["D:\\codes\\mine\\git\\ufs.git\\trunk\\prodRoot\\mongodb.bat"])
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()