# _*_ coding: utf-8 _*_
from Tkinter import *
from ScrolledText import *
import tkMessageBox
from tkFileDialog import *
import fileinput
t1=[]
root=None
def die():
    sys.exit(0)
def about():
    tkMessageBox.showinfo("Tkeditor","V1.0\n"
       "written in 2007\n"
       "writer:屈浩")

class editor:
    def __init__(self,rt):
        if rt==None:
            self.t=Tk()
        else:
            self.t=Toplevel(rt)
        self.t.title("Tkeditor %d"%len(t1))
        self.bar=Menu(rt)

        self.filem=Menu(self.bar)
        self.filem.add_command(label="打开",command=self.openfile)
        self.filem.add_command(label="新建",command=neweditor)
        self.filem.add_command(label="保存",command=self.savefile)
        self.filem.add_command(label="关闭",command=self.close)
        self.filem.add_separator()
        self.filem.add_command(label="退出",command=die)

        self.helpm=Menu(self.bar)
        self.helpm.add_command(label="关于",command=about)
        self.bar.add_cascade(label="文件",menu=self.filem)
        self.bar.add_cascade(label="帮助",menu=self.helpm)
        self.t.config(menu=self.bar)

        self.f=Frame(self.t,width=512)
        self.f.pack(expand=1,fill=BOTH)

        self.st=ScrolledText(self.f,background="white")
        self.st.pack(side=LEFT,fill=BOTH,expand=1)

    def close(self):
        self.t.destroy()

    def openfile(self):
        p1=END
        oname=askopenfilename(filetypes=[("Python file","*.*")])
        if oname:
            for line in fileinput.input(oname):
                self.st.insert(p1,line)
            self.t.title(oname)

    def savefile(self):
        sname=asksaveasfilename()
        if sname:
            ofp=open(sname,"w")
            ofp.write(self.st.get(1.0,END))
            ofp.flush()
            ofp.close()
            self.t.title(sname)

def neweditor():
    global root
    t1.append(editor(root))

if __name__=="__main__":
    root=None
    t1.append(editor(root))
    root=t1[0].t
    root.mainloop()