
#From http://www.alarmchang.com/wiki/index.php?title=Python_kill_process_by_Name_%E6%96%B9%E6%B3%95%E4%BA%8C%E4%BD%BF%E7%94%A8_win32api.TerminateProcess
"""
find out process name which is "noteapd" and kill them all.
"""
import win32api, win32pdhutil, win32con, sys
 
def killProcName(procname):
	# Change suggested by Dan Knierim, who found that this performed a
	# "refresh", allowing us to kill processes created since this was run
	# for the first time.
	try:
		win32pdhutil.GetPerformanceAttributes('Process','ID Process',procname)
	except:
		pass
 
	pids = win32pdhutil.FindPerformanceAttributesByName(procname)
	print pids
	if len(pids)==0:
		result = "Can't find %s" % procname
	elif len(pids)>=1:
		for sPids in pids:
			print sPids
			handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0,sPids)
			win32api.TerminateProcess(handle,0)
			win32api.CloseHandle(handle)
 
if __name__ == '__main__':
	killProcName("notepad")#notepad.exe