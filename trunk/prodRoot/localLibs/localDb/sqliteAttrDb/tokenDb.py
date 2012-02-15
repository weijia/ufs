#from dbBackend import *
import sys
import sqlite3 as sqlite

import configuration
#from logSys import *


class tokenDb:
  def __init__(self, tokenDbPath):
    self.tokenDbPath = tokenDbPath

  def getid(self, token):
    #Open database
    tokenCur, tokenDb = self.openDb()
    #Check if token has ' or ", need to change ' to '', " need not be changed
    #print type(token)
    #token = unicode(token)
    if (type(token) == unicode) or (type(token) == str):
      token = token.replace("\'","\'\'")
      #print 'relacing token:%s'%token
      token = token.encode('utf8')
    #ncl(type(token))
    #Check if the token exists
    query_cmd = 'SELECT * from token WHERE token = \'%s\' ORDER BY token ASC'%token
    #cl(query_cmd.decode('utf8'))
    result = tokenCur.execute(query_cmd)
    for e in result:
      #print e[0]
      return e[0]
    #Token does not exist, create one
    query_cmd = 'INSERT INTO token(token, create_date) VALUES (\'%s\', DATETIME(\'NOW\'))'%token
    #print query_cmd
    result = tokenCur.execute(query_cmd)
    tokenDb.commit()
    #Get the created token's ID
    query_cmd = 'SELECT * from token WHERE token = \'%s\' ORDER BY token ASC'%token
    #print query_cmd
    result = tokenCur.execute(query_cmd)
    for e in result:
      return e[0]

  def get(self, tokenid):
    #Open database
    tokenCur, tokenDb = self.openDb()
    query_cmd = 'SELECT * from token WHERE id = %d ORDER BY token ASC'%tokenid
    #print query_cmd
    result = tokenCur.execute(query_cmd)
    for e in result:
      #print e[0]
      #print e
      return e[1]
    raise "Token ID does not exist"

#The following function(s) is only for internal use
  def openDb(self):
    tokenDb = sqlite.connect(self.tokenDbPath)
    tokenCur = tokenDb.cursor()
    try:
      create_cmd = 'CREATE TABLE token (id INTEGER PRIMARY KEY\
      , token VARCHAR(512)\
      , create_date DATE)'
      #print create_cmd
      tokenCur.execute(create_cmd)
      tokenDb.commit()
    except sqlite.OperationalError:
      #The table does not exist, create table
      #print "exist"
      pass
    return tokenCur, tokenDb

def main():
    db = tokenDb(configuration.defaultTokenDbPath)
    print db.getid('helloworld')
    print db.getid('goodbyeworld')
    print db.getid('helloworld')
    print db.getid('goodbyeworld')
    print db.get(1)
    print db.get(2)


   
if __name__ == '__main__':
    main()

