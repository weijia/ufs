import sys
sys.path.append('D:\\codes\\python\\weijia_ufs\\prodRoot')
#print sys.path

#reference: http://wiki.wxpython.org/cx_freeze
#http://cx-freeze.sourceforge.net/cx_Freeze.html

includes = ['pango', 'pangocairo']
includefiles = [('gtkClipManager.glade', 'gtkClipManager.glade')]
excludefiles = []
'''
includefiles = [("localLibs\\logWin\\gf-16x16.png", "gf-16x16.png"),
                    ("localLibs\\logWin\\consoleWnd.glade", "consoleWnd.glade"), "etc",
                    ("C:\\Program Files\\Gtk+\\lib\\gtk-2.0\\2.10.0\\loaders", "loaders"),
                    ("..\\otherBin", "."),
                    ("C:\\WINDOWS\\system32\\zlib1.dll", "zlib1.dll")
               ]
               
excludefiles = ["libdbus-1.dll", "libdbus-glib-1.dll"]
'''
from cx_Freeze import setup, Executable
setup(name = "gtkClipManager",
        version = "0.1",
        description = "Simple clip manager",
        executables =   [
                         Executable("gtkClipManager.py"),
                         #Executable("dbusTest.py"),
                         #Executable("desktopApp\\onlineSync\\encytpedZipSyncTaskV2.py", path = 'D:\\codes\\python\\weijia_ufs\\prodRoot')
                        ],
        options =   {"build_exe":   {"includes":includes, 'include_files':includefiles, "bin_excludes":excludefiles, 
                                "build_exe":"d:\\tmp\\build\\gtkClipManager\\",
                                #"build_exe":"d:\\tmp\\syncbuild",
                                #"base": "Win32GUI"
                    }},
      )