import sys
import win32com.client
import os

def createPythonShortcut(shortcutPath, pythonScriptPath, pythonExecPath='c:/python25/python.exe')
  if os.path.exists(pythonScriptPath):
    if not os.path.isdir(pythonScriptPath)
      shell = win32com.client.Dispatch("WScript.Shell")
      shortcut = shell.CreateShortCut(shortcutPath)
      shortcut.Targetpath = pythonExecPath
      shortcut.WorkingDirectory = os.path.dirname(pythonScriptPath)
      shortcut.Arguments = pythonScriptPath
      shortcut.save()
