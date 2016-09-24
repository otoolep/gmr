import httplib2
import csv
import os
import sys
import argparse
import base64
from email.mime.text import MIMEText
from apiclient import discovery, errors
import oauth2client


SENDER = "Philip O'Toole <philip@percolate.com>"
TITLE = 'Director of Data Platform Engineering'
SUBJECT = 'Data Platform and Analytics at Percolate'

def get_credentials(credential_path):
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        return None
    return credentials


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    return service.users().messages().send(userId=user_id, body=message).execute()

def load_recipients(path):
    """
    Load a recipient file
    Args:
        path: path to recipients file.

    Returns:
        list of dictionary objects
    """
    recipients = []
    with open(path, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        for l in lines:
            recipients.append({'name': l[0], 'email': l[1], 'message-ref': [2]})
    return recipients


def load_messages(path):
    """
    Load a messages file.
    Args:
        path: path to messages file

    Returns:
        dictionary of messages
    """
    messages = {}
    with open(path, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        for l in lines:
            messages[l[0]] = l[1]
    return messages

def compose(recipient, message, sender):
    """
    Compose a single email message
    Args:
        recipient: addressee name
        message: message body
        sender: send name
    Returns:
        full message
    """
    return 'Hello %s,\n\n%s\n\n%s' % (recipient, message, sender)


def parse_args():
    # Create default credential path.
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'gmail-python.json')

    parser = argparse.ArgumentParser(description='Send some emails')
    parser.add_argument('recipients', metavar='R', type=str,
                        help='CSV file of name,email,message-ref')
    parser.add_argument('messages', metavar='C', type=str,
                        help='CSV file of message-ref,message')
    parser.add_argument('--creds', metavar='FILE', type=str,
                        default=credential_path,
                        help='path to credentials file, default: %s' % credential_path)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    credentials = get_credentials(args.creds)
    if credentials is None:
        print 'Failed to get credentials'
        sys.exit(1)

    recipients = load_recipients(args.recipients)
    print '%d receipients loaded.' % len(recipients)

    messages = load_messages(args.messages)
    print '%d messages loaded.' % len(messages)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # Send each e-mail.
    for r in recipients:
        body = compose(r['name'], messages[r['message-ref']], 'Philip%s' % TITLE)
        m = create_message("Philip O'Toole <philip@percolate.com>", r['email'], SUBJECT, body)
        # XXX DO A CONFIRM STEP HERE
        send_message(service, 'me', m)
        print 'Message sent to %s' % r['email']


if __name__ == '__main__':
    main()

