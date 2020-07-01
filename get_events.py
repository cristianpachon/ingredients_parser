from get_credentials import get_credentials
import datetime
import warnings
import pytz

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

    print(calendar_wanted['id'])
       
    return calendar_wanted


def transform_to_madrid_timestamp(date, is_end_date):
    time_to_add = '23:59:59' if is_end_date else '00:00:00'
    date_format ='{} {}'.format(date, time_to_add)
    return datetime.datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('Europe/Madrid')).isoformat('T')

def get_events(calendar, date_ini = None, date_end = None):
    datetime_ini = transform_to_madrid_timestamp(date=date_ini, is_end_date=False)
    datetime_end = transform_to_madrid_timestamp(date=date_end, is_end_date=True)

    # zzz: why us giving events before the datetime_ini
    
    print(datetime_ini, datetime_end)
    calendar_info = get_calendar(calendar)

    events = service.events().list(calendarId=calendar_info['id'], 
                                timeMin=datetime_ini, 
                                timeMax=datetime_end).execute()

    return events
    


print(get_events(calendar='Àpats', 
                date_ini = '2020-07-01',
                date_end = '2020-07-01'))
