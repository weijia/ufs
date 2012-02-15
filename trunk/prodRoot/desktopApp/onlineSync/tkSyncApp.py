import Tkinter
import tkFileDialog
import configDict
#import StringVar
import tkMessageBox
import sys

textStr = {"originalDir": "Original directory:", "archiveDir": "Archive directory:", 
                    "selectDir": "Select directory", "workingDir":"Working directory", "passWd":"Password:"}


import encytpedZipSync

class dirSelector:
    def __init__(self, txtWidget, top):
        self.txtWidget = txtWidget
        self.top = top
    def showDialog(self):
        dirname = tkFileDialog.askdirectory(parent = self.top, initialdir=self.txtWidget.get(),title='Pick a directory')
        self.txtWidget.set(dirname)
        #self.txtWidget.insert(0, dirname)


class tkSyncApp:
    def __init__(self):
        self.config = configDict.configFileDict('config.txt',{'srcDir':"", 'destDir':"", "workingDir":""})
    def run(self):
        self.top = Tkinter.Tk()
        top = self.top
        
        label1 = Tkinter.Label(top, text=textStr["originalDir"])
        self.srcTxt = Tkinter.StringVar()
        srcTextEntry = Tkinter.Entry(top, width = 50, textvariable = self.srcTxt)
        self.srcTxt.set(self.config["srcDir"])
        srcSelector = dirSelector(self.srcTxt, top)
        selectSrc = Tkinter.Button(top,text=textStr['selectDir'],command=srcSelector.showDialog,activeforeground='white',
    activebackground='red')
    
    
    
        label2 = Tkinter.Label(top, text=textStr["archiveDir"])
        self.dstTxt = Tkinter.StringVar()
        dstTextEntry = Tkinter.Entry(top, width = 50, textvariable = self.dstTxt)
        self.dstTxt.set(self.config["destDir"])
        dstSelector = dirSelector(self.dstTxt, top)
        selectDst = Tkinter.Button(top,text=textStr['selectDir'],command=dstSelector.showDialog,activeforeground='white',
    activebackground='red')

    
        label3 = Tkinter.Label(top, text=textStr["workingDir"])
        self.workingDirTxt = Tkinter.StringVar()
        workingDirTextEntry = Tkinter.Entry(top, width = 50, textvariable = self.workingDirTxt)
        self.workingDirTxt.set(self.config["workingDir"])
        srcSelector = dirSelector(self.workingDirTxt, top)
        selectWorking = Tkinter.Button(top,text=textStr['selectDir'],command=srcSelector.showDialog,activeforeground='white',
    activebackground='red')
    
        label4 = Tkinter.Label(top, text=textStr["passWd"])
        self.passwdTxt = Tkinter.StringVar()
        passwdTextEntry = Tkinter.Entry(top, width = 50, textvariable = self.passwdTxt)
        passwdTextEntry["show"] = "*"
        
        label1.pack()
        srcTextEntry.pack()
        selectSrc.pack()
        label2.pack()
        dstTextEntry.pack()
        selectDst.pack()
        label3.pack()
        workingDirTextEntry.pack()
        selectWorking.pack()
        label4.pack()
        passwdTextEntry.pack()
        
        syncBut = Tkinter.Button(top,text='Sync',command=self.sync,activeforeground='white',
    activebackground='red')
        quit = Tkinter.Button(top,text='QUIT',command=top.quit,activeforeground='white',
    activebackground='red')
        syncBut.pack()
        # quit.pack()
        self.top.protocol("WM_DELETE_WINDOW", self.saveConfigAndQuit)
        
        Tkinter.mainloop()


    def saveConfigAndQuit(self):
        self.config["srcDir"] = self.srcTxt.get()
        self.config["destDir"] = self.dstTxt.get()
        self.config["workingDir"] = self.workingDirTxt.get()
        self.config.store()
        if True:#tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            #root.destroy()
            self.top.destroy()
    
    def sync(self):
        self.callSyncObj(self.srcTxt.get(), self.passwdTxt.get(), self.dstTxt.get(), self.workingDirTxt.get())
    
    def callSyncObj(self, folder = "d:/tmp/test/source", encryptionPass = "default pass", zipDir = "d:/tmp/test/zip", 
                workingPath = "d:/tmp/test/working", test = False):
        e = encytpedZipSync.encSyncTask(str(sys.argv[0:]))
        if test == "test":
            passwd = "testPass"
        else:
            passwd = encryptionPass
        e.initParam(zipDir, folder, workingPath, passwd, "extract")
        e.run()
        e = encytpedZipSync.encSyncTask(str(sys.argv[0:]))
        if test:
            passwd = "testPass"
            zipDir = "d:/tmp/test/zip"
            folder = "d:/tmp/test/source"
            workingPath = "d:/tmp/test/working"
        else:
            passwd = encryptionPass
        e.initParam(zipDir, folder, workingPath, passwd, "sync")
        e.run()

        
if __name__ == "__main__":
    a = tkSyncApp()
    a.run()