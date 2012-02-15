import urllib
import libSys
import libs.ufsDb.ufsClient



def main():
  u = libs.ufsDb.ufsClient.ufsClient()
  u.login('test1', 'testpass')
  print u.uid
  
if __name__ == '__main__':
    main()

