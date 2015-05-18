import datetime
import os

from apiclient.discovery import build
import argparse
from httplib2 import Http
import oauth2client
from pygoogle import pygoogle
import rfc3339


APPLICATION_NAME = 'Shellper'
CLIENT_SECRET_FILE = 'etc/client_secret.json'
CREDENTIALS_PATH = 'etc/calendar-api.json'
SCOPES = 'https://www.googleapis.com/auth/calendar'


class Base(object):
    def __init__(self):
        self.page_number = 1
        self.service = None

    def _init_service(self):
        credentials = self.authentication()
        return build('calendar', 'v3',
                     http=credentials.authorize(Http()))

    def convert_to_rfc3339(self, datelist, timelist, inc=0):
        return rfc3339.rfc3339(datetime.datetime(datelist[2],
                                                 datelist[1],
                                                 datelist[0],
                                                 hour=timelist[0]+inc,
                                                 minute=timelist[1]))

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
        self.service = self._init_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print 'Getting the upcoming 10 events'
        eventsResult = self.service.events().list(
            calendarId='primary',
            maxResults=10, singleEvents=True, timeMin=now,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print 'No upcoming events found.'
        for event in events:
            start = event['start'].get('dateTime')
            print start, event['summary']

    def create_event(self, config):
        if self.service is None:
            self.service = self._init_service()
        datelist = config["date"].split(".")
        datelist = map(int, datelist)
        timelist = config["time"].split(":")
        timelist = map(int, timelist)
        try:
            datelist[2]
        except IndexError:
            datelist.append(datetime.date.today().year)
        event = {
            'summary': config["summary"],
            'start': {
                'dateTime': self.convert_to_rfc3339(datelist, timelist)
            },
            'end': {
                'dateTime': self.convert_to_rfc3339(datelist, timelist, inc=1)
            },
            'description': ' '.join(config["description"][0]).replace(" ",
                                                                      "\n")
        }

        created_event = self.service.events().insert(calendarId='primary',
                                                     body=event).execute()
        return created_event['id']

    def delete_event(self, eventId):
        self.service.events().delete(calendarId='primary',
                                     eventId=eventId).execute()
