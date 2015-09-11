import datetime
import os

from apiclient.discovery import build
import argparse
import base64
from email.mime.text import MIMEText
import httplib2
import oauth2client
import pygoogle
import re
import rfc3339


APPLICATION_NAME = 'shellper'
CALENDAR_CLIENT_SECRET_FILE = 'etc/client_secret_calendar.json'
GMAIL_CLIENT_SECRET_FILE = 'etc/client_secret_gmail.json'
CALENDAR_CREDENTIALS_PATH = 'etc/calendar-api.json'
GMAIL_CREDENTIALS_PATH = 'etc/gmail-api.json'
CALENDAR_SCOPES = 'https://www.googleapis.com/auth/calendar'
GMAIL_SCOPES = 'https://www.googleapis.com/auth/gmail.send'


# Base class for working of app
class Base(object):
    def __init__(self):
        self.page_number = 1
        self.service = None

    def _init_service(self, service='calendar', version='v3'):
        credentials = self.authentication_in(service)
        return build(service, version,
                     http=credentials.authorize(httplib2.Http()))

    def convert_to_rfc3339(self, datelist, timelist, inc=0):
        return rfc3339.rfc3339(datetime.datetime(datelist[2],
                                                 datelist[1],
                                                 datelist[0],
                                                 hour=timelist[0] + inc,
                                                 minute=timelist[1]))

    # Add results to event description
    def add_links(self, event):
        event["description"] = []
        if self.search_query(event["summary"]):
            event["description"].append(self.search_query(
                event["summary"]))
        else:
            event["description"].append(["Results_not_found"])

    # Search query in google.com
    def search_query(self, query):
        request = pygoogle.pygoogle(query)
        request.pages = self.page_number
        return request.get_urls()

    # Check of available access to user calendar,
    # if access unavailable - request access
    def authentication_in(self, service):
        flags = argparse.ArgumentParser(
            parents=[oauth2client.tools.argparser]).parse_args()
        home_dir = os.path.expanduser('shellper')
        credential_dir = os.path.join(home_dir, 'etc/.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        CLIENT_SECRET_FILE = CALENDAR_CLIENT_SECRET_FILE
        SCOPES = CALENDAR_SCOPES
        CREDENTIALS_PATH = CALENDAR_CREDENTIALS_PATH

        if service is 'gmail':
            SCOPES = GMAIL_SCOPES
            CLIENT_SECRET_FILE = GMAIL_CLIENT_SECRET_FILE
            CREDENTIALS_PATH = GMAIL_CREDENTIALS_PATH
        store = oauth2client.file.Storage(CREDENTIALS_PATH)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = oauth2client.client.flow_from_clientsecrets(
                CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = oauth2client.tools.run_flow(flow, store, flags)
            print 'Storing credentials to %s' % CREDENTIALS_PATH
        return credentials

    def create_mail(self, config, to):
        self.add_links(config)
        links = config.get('description')[0]
        body = '\n'.join([str(link) for link in links])
        message = MIMEText(body)
        message['to'] = to
        message['from'] = 'handbox.inc@gmail.com'
        message['subject'] = config.get('summary')
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def send_mail(self, config, to):
        service = self._init_service(service='gmail', version='v1')
        message = service.users().messages().send(
            userId='me',
            body=self.create_mail(config, to)).execute()
        print 'Sent Message Id: %s' % message['id']
        return message

    # List of events from available account
    def get_event_list(self):
        self.service = self._init_service()
        now = '%sZ' % datetime.datetime.utcnow().isoformat()
        print 'Getting the upcoming 10 events'
        eventsResult = self.service.events().list(
            calendarId='primary',
            maxResults=10, singleEvents=True, timeMin=now,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        event_list = []
        for event in events:
            start = event['start'].get('dateTime')
            new_event = (start, event['summary'])
            event_list.append(new_event)

        return event_list

    # Create event from file etc/template.yaml
    # Parse date format 00-00-0000, 00/00/0000, 00.00.0000; time formats 00.00,
    # 00-00, 00:00
    # TODO(esikachev): fix comment when implement UI

    def create_event(self, config):
        if self.service is None:
            self.service = self._init_service()
        self.add_links(config)
        datelist = re.split(r'[./-]', config["date"])
        datelist = map(int, datelist)
        timelist = re.split(r'[.:-]', config["time"])
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

    def quick_create_event(self, config):
        self.service = self._init_service()
        created_event = self.service.events().quickAdd(
            calendarId='primary', text=config["summary"]).execute()

        return created_event['id']

    # Delete event on id
    def delete_event(self, eventId):
        self.service.events().delete(calendarId='primary',
                                     eventId=eventId).execute()
