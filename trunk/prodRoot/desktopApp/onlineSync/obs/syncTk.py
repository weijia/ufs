import Tkinter
import tkFileDialog
import configDict
#import StringVar
import tkMessageBox
import sys

textStr = {"originalDir": "Original directory:", "archiveDir": "Archive directory:", "selectDir": "Select directory"}
import encytpedZipSync
class quitAction:
    def __init__(self, top):
        self.top = top
    def callback(self):
        if True:#try:
            self.handler()
        else:#except:
            pass
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            #root.destroy()
            self.top.destroy()
    def handler(self):
        pass
            
class saveConfigQuitAction(quitAction):
    def __init__(self, top, config, entry1, entry2):
        self.top = top
        self.config = config
        self.entry1 = entry1
        self.entry2 = entry2
    def handler(self):
        self.config["srcDir"] = self.entry1.get()
        self.config["destDir"] = self.entry2.get()
        self.config.store()
            
class dirSelector:
    def __init__(self, txtWidget, top):
        self.txtWidget = txtWidget
        self.top = top
    def showDialog(self):
        dirname = tkFileDialog.askdirectory(parent = self.top, initialdir=self.txtWidget.get(),title='Pick a directory')
        self.txtWidget.set(dirname)
        #self.txtWidget.insert(0, dirname)

        
        
def startSync(folder = "d:/tmp/test/source", encryptionPass = "default pass", zipDir = "d:/tmp/test/zip", 
            workingPath = "d:/tmp/test/working",direction = "sync", test = "test"):
    e = encytpedZipSync.encSyncTask(str(sys.argv[0:]))
    if test == "test":
        passwd = "testPass"
    else:
        passwd = encryptionPass
    e.initParam(zipDir, folder, workingPath, passwd, "extract")
    e.run()
    e = encytpedZipSync.encSyncTask(str(sys.argv[0:]))
    if test == "test":
        passwd = "testPass"
    else:
        passwd = encryptionPass
    e.initParam(zipDir, folder, workingPath, passwd, "sync")
    e.run()
        
#Ref: http://blog.sina.com.cn/s/blog_4b5039210100eoq7.html
def main():
    top = Tkinter.Tk()
    config = configDict.configFileDict('config.txt',{'srcDir':"", 'destDir':""})
    label1 = Tkinter.Label(top, text=textStr["originalDir"])
    srcTxt = Tkinter.StringVar()
    srcTextEntry = Tkinter.Entry(top, width = 50, textvariable = srcTxt)
    srcTxt.set(config["srcDir"])
    srcSelector = dirSelector(srcTxt, top)
    selectSrc = Tkinter.Button(top,text=textStr['selectDir'],command=srcSelector.showDialog,activeforeground='white',
activebackground='red')
    label2 = Tkinter.Label(top, text=textStr["archiveDir"])
    dstTxt = Tkinter.StringVar()
    dstTextEntry = Tkinter.Entry(top, width = 50, textvariable = dstTxt)
    dstTxt.set(config["destDir"])
    dstSelector = dirSelector(dstTxt, top)

    selectDst = Tkinter.Button(top,text=textStr['selectDir'],command=dstSelector.showDialog,activeforeground='white',
activebackground='red')

    label1.pack()
    srcTextEntry.pack()
    selectSrc.pack()
    label2.pack()
    dstTextEntry.pack()
    selectDst.pack()
    
    quitActionHandler = saveConfigQuitAction(top, config, srcTxt, dstTxt)
    
    syncBut = Tkinter.Button(top,text='Sync',command=startSync,activeforeground='white',
activebackground='red')
    quit = Tkinter.Button(top,text='QUIT',command=top.quit,activeforeground='white',
activebackground='red')
    syncBut.pack()
    quit.pack()
    
    

if __name__ == "__main__":
    main()