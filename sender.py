import httplib2
import os
import sys
import argparse

import service
import loaders
import message

SENDER = "Philip O'Toole <philip@percolate.com>"
SUBJECT = 'Data Platform, Analytics, and Search role at Percolate'


def yes_or_no(question):
    reply = str(raw_input(question+' (y/N): ')).lower().strip()
    if reply != '' and reply[0] == 'y':
        return True
    return False


def parse_args():
    # Create default credential path.
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    credential_path = os.path.join(credential_dir, 'gmail-python.json')

    parser = argparse.ArgumentParser(description='Send some emails')
    parser.add_argument('recipients', metavar='R', type=str,
                        help='comma-seperated file of name,email,message-ref')
    parser.add_argument('messages', metavar='C', type=str,
                        help='|-seperated file of message-ref,message')
    parser.add_argument('footer', metavar='F', type=str,
                        help='footer file')
    parser.add_argument('--creds', metavar='FILE', type=str,
                        default=credential_path,
                        help='path to credentials file, default: %s' % credential_path)
    parser.add_argument('--force', action="store_true",
                        default=False,
                        help='send emails without asking for confirmation')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    credentials = service.get_credentials(args.creds)
    if credentials is None:
        print 'Failed to get credentials'
        sys.exit(1)
    print 'Credentials successfully retrieved.'

    serv = service.Service(credentials)
    agent = message.Agent(serv)

    composer = loaders.Composer(args.recipients, args.messages, args.footer, SENDER, SUBJECT)
    lr, lm = composer.open()
    print '%d recipients loaded, %d messages loaded.' % (lr, lm)

    for m in composer:
        print '\n=========================================================\n\n'
        if not args.force:
            print m
            if not yes_or_no('Send email?'):
                continue

        agent.send(m)
        print 'Email sent to %s' % m.to

    composer.close()


if __name__ == '__main__':
    main()

