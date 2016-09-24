import base64
from email.mime.text import MIMEText


class Message(object):
    def __init__(self, sender, to, subject, body):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.body = body

    def __str__(self):
        print 'TO:      %s' % self.to
        print 'FROM:    %s' % self.sender
        print 'SUBJECT: %s' % self.subject
        print
        print self.body
        print


class Agent(object):
    def __init__(self, service):
        self.service = service

    def send(self, message):
        m = MIMEText(message.body)
        m['to'] = message.to
        m['from'] = message.sender
        m['subject'] = message.subject
        e = {'raw': base64.urlsafe_b64encode(m.as_string())}
        self.service.send(e)



