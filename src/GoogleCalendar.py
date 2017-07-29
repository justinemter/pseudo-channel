from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import os.path as path
import sys

import datetime

"""try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None"""


class GoogleCalendar():

    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    two_up =  path.abspath(path.join(__file__ ,"../../../"))
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, 'client_secret.json')
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = credential_dir
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    KEY = ''

    def __init__(self, key):

        self.KEY = key

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def get_entries(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

        end = (datetime.datetime.utcnow() + datetime.timedelta(hours=24))

        end = end.isoformat() + 'Z' # 'Z' indicates UTC time

        #print(now)

        #print(end)

        print('##### Getting the upcoming calendar events')
        eventsResult = service.events().list(
            calendarId=self.KEY, timeMin=now, timeMax=end, maxResults=250, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            #start = event['start'].get('dateTime', event['start'].get('date'))
            #print(start, event['summary'])
            pass
        return events


if __name__ == '__main__':
    pass