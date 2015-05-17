import argparse
from pygoogle import pygoogle
import os
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient.discovery import build
from datetime import datetime
from httplib2 import Http

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'shellper/etc/client_secret.json'
APPLICATION_NAME = 'Shellper'


class Base(object):

    def __init__(self):
        self.page_number = 1

    def search_query(self, query):
        request = pygoogle(query)
        request.pages = self.page_number
        return request.get_urls()

    def authentication(self):
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-api.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    def get_event_list(self):
        credentials = self.authentication()
        service = build('calendar', 'v3', http=credentials.authorize(Http()))
        now = datetime.utcnow().isoformat() + 'Z'
        print 'Getting the upcoming 10 events'
        eventsResult = service.events().list(
            calendarId='primary',
            maxResults=10, singleEvents=True, timeMin=now,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print 'No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime')
            print start, event['summary']
