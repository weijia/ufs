import pygtk
pygtk.require('2.0')
import gtk
import os
#import gtkTaskbarIconForConsole
#import gtkTxtWndMod
import localLibSys
import localLibs.logSys.logDir as logDir
import beanstalkc
from localLibs.services.beanstalkdServices.beanstalkServiceBaseV2 import gBeanstalkdServerHost, gBeanstalkdServerPort
from localLibs.logWin.gui.GtkTaskBarIconApp import GtkTaskBarIconApp
import localLibs.logWin.gui.fileTools as fileTools
from localLibs.logWin.gui.ConsoleOutputWnd import ConsoleOutputWnd
from ConsoleOutputCollector import ConsoleOutputCollector
from localLibs.logSys.logSys import *
import gobject

class LauncherMain(GtkTaskBarIconApp):
    '''
    This class will generate the floating element and the task bar icon.
    '''
    def __init__(self):
        super(LauncherMain, self).__init__()
        self.app_name_to_task_dict = {}
        #self.basic_app_name_to_task_dict = {}
        self.wnd_to_console_dict = {}
        self.task_to_menu_item_dict = {}
        self.start_basic_service()
        self.drop_handler = None
    
    #####################################
    # Event handlers
    #####################################
    def on_menu_clicked(self, menu_text):
        self.app_name_to_task_dict[menu_text].show()

    def on_quit_clicked(self):
        #self.window.hide()
        #self.icon.set_visible(False)
        print 'on_quit_clicked'
        for i in self.task_to_menu_item_dict.keys():
            if i == self.beanstalkd_app:
                continue
            i.send_stop_signal()
        print 'wait for 10 seconds'
        self.timer_id = gobject.timeout_add(50000, self.final_quit)#Here time value are milliseconds
        

        
    def on_dropped(self, wid, context, x, y, data, info, time):
        if not (self.drop_handler is None):
            self.drop_handler.on_dropped(wid, context, x, y, data, info, time)
        else:
            print data.data
        
    def console_wnd_close_clicked(self, console_wnd):
        self.wnd_to_console_dict[console_wnd].send_stop_signal()
        #self.timer_id = gobject.timeout_add(5000, self.kill_console_process_tree)#Here time value are milliseconds
    
    ###############################
    # Internal functions
    ###############################
    def register_drop_handler(self, handler):
        self.drop_handler = handler
        
    def final_quit(self):
        print 'start to killing apps'
        #Kill Beanstalkd Launcher service
        self.beanstalkd_launcher.kill_console_process_tree()
        
        for i in self.task_to_menu_item_dict.keys():
            if i == self.beanstalkd_app:
                continue
            i.kill_console_process_tree()
        
        
        
        if not (self.beanstalkd_app is None):
            self.beanstalkd_app.kill_console_process_tree()
        
        gtk.main_quit()
        time.sleep(5)
        print 'all application killed, after main_quit'
        exit(0)
    def start_services(self, app_list):
        for i in app_list:
            self.start_basic_app(i)
    
    
    def start_basic_service(self):
        self.beanstalkd_app = self.start_basic_app('startBeanstalkd.bat')
        if self.beanstalkd_app is None:
            return None
        #Check if beanstalkd started correctly
        retry_cnt = 0
        while True:
            try:
                self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
                break
            except beanstalkc.SocketError:
                retry_cnt += 1
                if retry_cnt > 100:
                    print "beanstalkd start failed"
                    break
        ###########################
        # Start mongodb
        ###########################
        self.mongodb_app = self.start_basic_app('mongodb.bat')
        if self.mongodb_app is None:
            return None
        #Check if beanstalkd started correctly
        retry_cnt = 0
        from pymongo import Connection
        from pymongo.errors import AutoReconnect
        while True:
            try:
                connection = Connection()
                break
            except AutoReconnect:
                retry_cnt += 1
                if retry_cnt > 100:
                    print "mongodb start failed"
                    break
        
        ###########################
        # Start beanstalkd service manager
        ###########################
        self.beanstalkd_launcher = self.start_basic_app("BeanstalkdLauncherService")
        
    def create_console_wnd_for_app(self, param):
        '''
        Start an app with full path and parameters passed in a list
        param: [appFullPath, param1, param2, ...]
        '''
        l = logDir.logDir(str(param))
        t = ConsoleOutputWnd(self, l.getLogFilePath())
        collector = ConsoleOutputCollector()
        cwd = localLibSys.get_root_dir()
        collector.runConsoleApp(t, cwd, param)
        self.wnd_to_console_dict[t] = collector
        
        
        cnt = 1
        app_name = os.path.basename(param[0])
        app_path = os.path.dirname(param[0])
        app_path_and_param_gen_str = "%s(%s) %s"%(app_name, app_path, str(param[1:]))
        if self.app_name_to_task_dict.has_key(app_path_and_param_gen_str):
            while self.app_name_to_task_dict.has_key(app_path_and_param_gen_str + '-' + str(cnt)):
                cnt +=1
            app_path_and_param_gen_str = app_path_and_param_gen_str + '-' + str(cnt)
          
        self.app_name_to_task_dict[app_path_and_param_gen_str] = t
        self.task_to_menu_item_dict[collector] = self.icon.addMenuItem(app_path_and_param_gen_str)
        return collector
        
        
    def start_basic_app(self, app_name):
        full_path = fileTools.findFileInProduct(app_name)
        if full_path is None:
            full_path = fileTools.findAppInProduct(app_name)
            if full_path is None:
                print app_name, 'not found ---- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                return None
        return self.create_console_wnd_for_app([full_path])
                
def main():
    g = LauncherMain()
    g.start_gui_msg_loop()

if __name__ == "__main__":
    main()
