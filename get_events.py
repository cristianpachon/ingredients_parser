from get_credentials import get_credentials
import datetime
import warnings

# Getting servie
service = get_credentials()


def get_calendar(calendar):
    calendars = service.calendarList().list().execute()

    calendar_wanted = None
    for cal in calendars['items']:
        if cal['summary'] == calendar:
            calendar_wanted = cal

    if calendar_wanted is None:
        warnings.warn('Calendar {} not Found'.format(calendar))
       
    return calendar_wanted


def get_events(calendar, datetime_ini = None, datetime_end = None):
    # zzz: why us giving events before the datetime_ini
    
    print(datetime_ini, datetime_end)
    calendar_info = get_calendar(calendar)

    events = service.events().list(calendarId=calendar_info['id'], 
                                timeMin=datetime_ini, 
                                timeMax=datetime_end).execute()

    return events
    


print(get_events(calendar='Àpats', 
                datetime_ini=datetime.datetime.utcnow().isoformat() + 'Z', 
                datetime_end=(datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'))
