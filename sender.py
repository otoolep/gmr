import httplib2
import csv
import os
import sys
import argparse
from apiclient import discovery, errors


SENDER = "Philip O'Toole <philip@percolate.com>"
TITLE = 'Director of Data Platform Engineering'
SUBJECT = 'Data Platform and Analytics at Percolate'





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

