from multiprocessing.managers import BaseManager
class QueueManager(BaseManager): pass

def launchScript(p):
    QueueManager.register('getLaunchQ')
    m = QueueManager(address=('localhost', 8809), authkey='abracadabra')
    m.connect()
    launchQ = m.getLaunchQ()
    launchQ.put(p)

import sys
    
def main():
    param = []
    for arg in sys.argv[1:]: 
        param.append(arg)
    if 0 == len(param):
        param = ['D:\\sandbox\\developing\\proxyRelay\\twistedProxy.py']
    launchScript(param)

if __name__ == "__main__":
    main()
