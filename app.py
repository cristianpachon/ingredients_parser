import argparse
from bin.calendar_manager import CalendarManager
from bin.parser import parse_meals


parser = argparse.ArgumentParser()
parser.add_argument('--date_ini')
parser.add_argument('--date_end')
parser.add_argument('--calendar_name')
args = parser.parse_args()
arguments = args.__dict__
calendar_name = arguments['calendar_name']
date_ini = arguments['date_ini']
date_end =arguments['date_end']

meals_calendar = CalendarManager(calendar_name)
events = meals_calendar.get_events(date_ini, date_end)

ingredients = parse_meals(events)

print(ingredients)
