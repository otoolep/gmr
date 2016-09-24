import csv

import message


class Composer(object):
    def __init__(self, recipients_file, messages_file, footer_file, sender, subject):
        self.rf = recipients_file
        self.mf = messages_file
        self.ff = footer_file
        self.sender = sender
        self.subject = subject
        self.recipients = []
        self.current_recipient = 0
        self.messages = {}
        self.footer = None

    def open(self):
        with open(self.rf, 'rb') as csvfile:
            lines = csv.reader(csvfile)
            for l in lines:
                self.recipients.append({'name': l[0], 'email': l[1], 'message_ref': l[2]})

        with open(self.mf, 'rb') as csvfile:
            lines = csv.reader(csvfile, delimiter='|')
            for l in lines:
                self.messages[l[0]] = l[1]

        with open(self.ff, 'rb') as f:
            self.footer = f.read()

        return len(self.recipients), len(self.messages)

    def close(self):
        pass

    def __iter__(self):
        return self

    def next(self):
        if self.current_recipient >= len(self.recipients):
            raise StopIteration

        r = self.recipients[self.current_recipient]
        m = self.messages[r['message_ref']]
        b = 'Hello %s,\n\n%s\n\n%s' % (r['name'], m, self.footer)

        self.current_recipient += 1
        return message.Message(self.sender, r['email'], self.subject, b)
