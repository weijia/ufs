import sys
sys.path.append('D:\\codes\\python\\weijia_ufs\\prodRoot')
#print sys.path
from cx_Freeze import setup, Executable
setup(name = "syncApp", version = "0.1", description = "Sync data from file to zip",
    executables = [Executable("encytpedZipSync.py"),Executable("tkSyncApp.py"),Executable("encytpedZipSyncTaskV2.py")],
    
    
    options =   {"build_exe":   {"build_exe":"d:\\apps\\python\\syncApp",
                            #"base": "Win32GUI"
                }},

    
)