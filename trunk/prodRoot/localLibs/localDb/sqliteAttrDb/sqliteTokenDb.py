import tokenDb


class sqliteTokenDb(tokenDb.tokenDb):
    def getId(self, token):
        return self.getid(token)
