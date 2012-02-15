import imaplib

class imapMailbox:
    def __init__(self, hostname = "127.0.0.1", username = "richard", password="123"):
        self.hostname = hostname
        self.username = username
        self.password = password
    def connect(self):
        self.connection = imaplib.IMAP4(self.hostname)
        # Login to our account
        self.connection.login(self.username, self.password)
        return self.connection
    def listInbox(self):
        self.connection.select("Inbox")
        self.connection.list()
        
    def create(self, mailboxName):
        '''
        Create a directory
        '''
        self.connection.create(mailboxName)
        
if __name__ == "__main__":
    i = imapMailbox()
    i.connect()
    i.create("hello")
    