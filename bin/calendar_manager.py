from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import warnings
import pytz


class CalendarManager:

    def __init__(self, calendar):
        self.calendar = calendar
        self.service = self.get_credentials()
        
        
    def get_credentials(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """

        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('credentials/token.pickle'):
            with open('credentials/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('credentials/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        return service


    def get_calendar(self):
        calendars = self.service.calendarList().list().execute()

        calendar_wanted = None
        for cal in calendars['items']:
            if cal['summary'] == self.calendar:
                calendar_wanted = cal

        if calendar_wanted is None:
            warnings.warn('Calendar {} not Found'.format(calendar))
        
        return calendar_wanted

    @staticmethod
    def transform_to_madrid_timestamp(date, is_end_date):
        time_to_add = '23:59:59' if is_end_date else '00:00:00'
        date_format ='{} {}'.format(date, time_to_add)
    
        return datetime.datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Europe/Madrid'))


    def _filter_events(self, events, ini, end):
        events_filtered = []
        for event in events['items']:
            event_start_time = datetime.datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            event_end_time = datetime.datetime.strptime(event['end']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
            if event_start_time>=ini and event_end_time<=end:
                events_filtered.append(event)
    
        return events_filtered

    def _get_summary_key(self, events):
        return [event['summary'] for event in events]


    def get_events(self, date_ini=None, date_end=None):
        datetime_ini = self.transform_to_madrid_timestamp(date=date_ini, is_end_date=False)
        datetime_end = self.transform_to_madrid_timestamp(date=date_end, is_end_date=True)
        
        calendar_info = self.get_calendar()
        
        raw_events = self.service.events().list(calendarId=calendar_info['id'], 
                                    timeMin=datetime_ini.isoformat('T'), 
                                    timeMax=datetime_end.isoformat('T')).execute()

        events_filtered = self._filter_events(events=raw_events, ini=datetime_ini, end=datetime_end)

        summary = self._get_summary_key(events_filtered)

        return summary
    