# -*- coding: utf-8 -*-  
#from QtGui import QTextBrowser
from PyQt4.QtGui import QApplication, QTextBrowser
import sys


def startQTextBrowser():
    browser = QTextBrowser() #ʵ����һ��textbrowser

    browser.append('sdfsdfds') #׷������

    browser.setOpenLinks(True) #���ĵ��ڲ����� Ĭ��ΪTrue

    browser.setOpenExternalLinks(True) #���ⲿ���� Ĭ��false ��openlinks����falseʱ ��ѡ����Ч

    #textbrowser.setSearchPaths(["ldks",":/sdfs"]) #�����ĵ�����·�� ����Ϊ����Ŀ¼��List

    #textbrowser.setSource("index.html") #�����ĵ�

    #dt=textbrowser.documentTitle() #�����ĵ��ı���

    #self.connect(textbrowser,SIGNAL("SourceChanged(QUrl)"),self.update) #����һ��SourceChanged(QUrl)�ź�

    browser.setDocumentTitle('dsds') #�����ĵ�����
    
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