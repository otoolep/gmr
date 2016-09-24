import httplib2
import os
import sys
import argparse

import service
import loaders
import message

SENDER = "Philip O'Toole <philip@percolate.com>"
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
    parser.add_argument('footer', metavar='F', type=str,
                        help='Footer file')
    parser.add_argument('--creds', metavar='FILE', type=str,
                        default=credential_path,
                        help='path to credentials file, default: %s' % credential_path)
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
    for m in composer:
        print m


if __name__ == '__main__':
    main()

