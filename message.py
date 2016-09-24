import base64
from email.mime.text import MIMEText


class Message(object):
    def __init__(self, sender, to, subject, body):
        self.sender = sender
        self.to = to
        self.subject = subject
        self.body = body

    def __str__(self):
        s = 'TO:      %s\nFROM:    %s\nSUBJECT: %s\n\n%s\n' % (self.sender, self.to, self.subject, self.body)
        return s


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



