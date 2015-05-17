from datetime import datetime
import os

from apiclient.discovery import build
import argparse
from httplib2 import Http
import oauth2client
from pygoogle import pygoogle


APPLICATION_NAME = 'Shellper'
CLIENT_SECRET_FILE = 'etc/client_secret.json'
CREDENTIALS_PATH = 'etc/calendar-api.json'
SCOPES = 'https://www.googleapis.com/auth/calendar'


class Base(object):

    def __init__(self):
        self.page_number = 1

    def search_query(self, query):
        request = pygoogle(query)
        request.pages = self.page_number
        return request.get_urls()

    def authentication(self):
        flags = argparse.ArgumentParser(
            parents=[oauth2client.tools.argparser]).parse_args()
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        store = oauth2client.file.Storage(CREDENTIALS_PATH)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(
                CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = oauth2client.tools.run_flow(flow, store, flags)
            else:
                credentials = oauth2client.tools.run(flow, store)
            print 'Storing credentials to ' + CREDENTIALS_PATH
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
