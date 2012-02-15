

from Tkinter import *


gAdditionalItems = [".."]

class tkFileSelector:
    def __init__(self, treeItem):
        self.curItem2NameMapping = None
        self.curName2Item = None
        self.curItemList = None
        self.curItem = None
        root = Tk()
        #Add scroll
        scrollbar = Scrollbar(root, orient=VERTICAL)

        listbox = Listbox(root, yscrollcommand=scrollbar.set)
        
        
        #Add scroll control
        scrollbar.config(command=listbox.yview)
        
        
        #listbox.insert(END, "a list entry")
        
        self.listbox = listbox
        self.tkSelectFile(treeItem)
        
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)



        listbox.bind("<Double-Button-1>", self.callback)

        root.mainloop()
        
    def callback(self, event):
        #print event.widget.curselection()
        if len(event.widget.curselection()) == 0:
            print 'no item'
            return
        #print self.curItemList
        i = int(event.widget.curselection()[0])
        print i
        if i < len(gAdditionalItems):
            if i == 0:
                #up a level
                print "parent of",self.curItem.itemId
                c = self.curItem.getContainerItem()
                print c.itemId
        else:
            c = self.curItem.child(self.curItemList[i-len(gAdditionalItems)])
        self.listbox.delete(0, END)
        self.tkSelectFile(c)


    def tkSelectFile(self, treeItem):
        '''
        for item in ["one", "two", "three", "four"]:
            listbox.insert(END, item)
        '''
        self.curItem2NameMapping = treeItem.listNamedChildren()
        self.curName2Item = {}
        self.curItemList = []
        self.curItem = treeItem
        print 'setting curItem', self.curItem.itemId
        print self.curItem.getContainerItem().itemId
        #print self.curItem2NameMapping
        for item in gAdditionalItems:
            self.listbox.insert(END, item)
        for item in self.curItem2NameMapping.keys():
            #print item, self.curItem2NameMapping[item]
            self.curName2Item[self.curItem2NameMapping[item]] = item
            self.curItemList.append(item)
            self.listbox.insert(END, self.curItem2NameMapping[item])
         

    
