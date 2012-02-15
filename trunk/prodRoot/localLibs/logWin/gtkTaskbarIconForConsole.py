#!/usr/bin/env python

import os
import gtk
#From http://fly-hyp.javaeye.com/blog/194821

import fileTools

class MyStatusIcon(gtk.StatusIcon):
        def __init__(self, parent):
                gtk.StatusIcon.__init__(self)
                menu = '''
                        <ui>
                         <menubar name="Menubar">
                          <menu action="Menu">
                           <separator/>
                           <menuitem action="About"/>
                           <separator/>
                           <menuitem action="Quit"/>
                          </menu>
                         </menubar>
                        </ui>
                '''
                actions = [
                        ('Menu',  None, 'Menu'),
                        ('About', gtk.STOCK_ABOUT, 'About', None, 'About', self.on_about),
                        ('Quit', gtk.STOCK_QUIT, 'Quit', None, 'Quit', self.on_quit)
                ]

                ag = gtk.ActionGroup('Actions')
                ag.add_actions(actions)
                self.manager = gtk.UIManager()
                self.manager.insert_action_group(ag, 0)
                self.manager.add_ui_from_string(menu)
                self.menu = self.manager.get_widget('/Menubar/Menu/About').props.parent
                iconFile = fileTools.findFileInProduct('gf-16x16.png')
                self.set_from_file(iconFile)
                self.set_tooltip('Console window for python applications')
                self.set_visible(True)
                #self.connect('activate', self.on_activate)
                self.connect('activate', self.on_popup_menu)
                self.connect('popup-menu', self.on_popup_menu)
                self.parent = parent
                self.actionTextMapping = {}
                
        def addMenuItem(self, menuText):
                copyStr = menuText
                menuActionName = copyStr.replace('"', '')
                #menuActionName = "testMenuAction"
                self.actionTextMapping[menuActionName] = menuText
                newMenu = u'''
                        <ui>
                         <menubar name="Menubar">
                          <menu action="Menu">
                           <menuitem action="%s" position="top"/>
                          </menu>
                         </menubar>
                        </ui>
                '''%menuActionName
                actions = [('%s'%menuActionName, None, menuText, None, 'open consle window', self.on_menuAction)]
                import uuid
                ag = gtk.ActionGroup(str(uuid.uuid4()))
                ag.add_actions(actions)
                self.manager.insert_action_group(ag, 0)
                return self.manager.add_ui_from_string(newMenu)

        def rmMenuItem(self, mergeId):
                self.manager.remove_ui(mergeId)
                
        def on_activate(self, data):
                #print 'on_activate'#Called when left mouse click
                pass

        def on_popup_menu(self, status, button, time):
                self.menu.popup(None, None, None, button, time)
        def on_menuAction(self, data):
                #print data.get_name()
                self.parent.clickM(self.actionTextMapping[data.get_name()])

        '''
        def on_action(self, data):
                self.newid = self.addMenuItem('good day')
        def on_action2(self, data):
                self.rmMenuItem(self.newid)
        '''
        def on_about(self, data):
                dialog = gtk.AboutDialog()
                dialog.set_name('Python Console Window')
                dialog.set_version('0.1')
                dialog.set_comments('Collect console logs for python console app')
                #dialog.set_website('http://kf701.cublog.cn')
                dialog.run()
                dialog.destroy()

        def on_quit(self, data):
                print 'Exit'
                self.set_visible(False)
                self.parent.close_application(None)
                #gtk.main_quit()
        def on_drop(self, data):
                print data.data
                
if __name__ == '__main__':
        icon = MyStatusIcon(None)
        #icon.drag_dest_set(0, [], 0)#Can not be called, as status icon is just a gobject, not a window
        #icon.connect('drag_drop', icon.on_drop)
        gtk.main()