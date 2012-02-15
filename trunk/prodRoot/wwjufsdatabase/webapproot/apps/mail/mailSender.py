import libs.html.response
import libs.platform.services
from google.appengine.api import mail


def sendMail(toMail, fileName = None, fileContent = None, mailSubject = "No title", mailBody = "No content"):
    if (fileName is None) or (fileContent is None):
        mail.send_mail(sender="googleaccount@gmail.com",
                      to=toMail,
                      subject=mailSubject,
                      body=mailBody)
    else:
        mail.send_mail(sender="googleaccount@gmail.com",
                  to=toMail,
                  subject=mailSubject,
                  body=mailBody,
                  attachments=[(fileName, fileContent)])

    
from libs.services.services import services

s = services()
h = s.getHtmlGen()
h.genHead()
f = s.getQuery()

    
#print f
if not f.has_key('uploadFile'):
  h.genForm('/apps/mail/mailSender.py',[['t','mailTo','googleaccount@gmail.com'],['f','uploadFile']])
else:
  #Process the file
  sendMail(f.get('mailTo','googleaccount@gmail.com'), 'attachment.txt',f['uploadFile'][0])
  h.redirect('/apps/mail/mailSender.py')
print '</body>'
h.genEnd()