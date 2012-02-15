import md5
import random

gMd5PassSplitter = u'.'

class userManager:
	def verifyPasswd(self, username, passwd, shoveLikeInst):
		try:
			md5PassWithTimeStamp = shoveLikeInst[username][0]
			md5Pass, timeStamp  = md5PassWithTimeStamp.split(gMd5PassSplitter)
			if unicode(str(md5.new(passwd+timeStamp).hexdigest())) == md5Pass:
				return True
			else:
				return False
		except KeyError:
			#Add new user
			random.seed()
			timeStamp = unicode(str(random.randint(0,10000000)))
			md5Pass = unicode(str(md5.new(passwd+timeStamp).hexdigest()))
			shoveLikeInst[username] = md5Pass + gMd5PassSplitter + timeStamp
			return True
			