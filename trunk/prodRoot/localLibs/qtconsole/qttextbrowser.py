# -*- coding: utf-8 -*-  
#from QtGui import QTextBrowser
from PyQt4.QtGui import QApplication, QTextBrowser
import sys


def startQTextBrowser():
    browser = QTextBrowser() #实例化一个textbrowser

    browser.append('sdfsdfds') #追加内容

    browser.setOpenLinks(True) #打开文档内部链接 默认为True

    browser.setOpenExternalLinks(True) #打开外部链接 默认false 当openlinks设置false时 该选项无效

    #textbrowser.setSearchPaths(["ldks",":/sdfs"]) #设置文档搜索路径 参数为包含目录的List

    #textbrowser.setSource("index.html") #设置文档

    #dt=textbrowser.documentTitle() #返回文档的标题

    #self.connect(textbrowser,SIGNAL("SourceChanged(QUrl)"),self.update) #发出一个SourceChanged(QUrl)信号

    browser.setDocumentTitle('dsds') #设置文档标题
    
    browser.show()
    return browser
    
from PyQt4 import QtGui

def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    b = startQTextBrowser()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()