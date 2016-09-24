import httplib2
import oauth2client


from apiclient import discovery


class Service(object):
    def __init__(self, credentials, user_id='me'):
        self.credentials = credentials
        self.user_id = user_id
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def send(self, e):
        self.service.users().messages().send(userId=self.user_id, body=e).execute()


def get_credentials(credential_path):
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        return None
    return credentials
