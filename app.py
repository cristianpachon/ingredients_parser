from bin.calendar_manager import CalendarManager
from bin.parser import parse_meals
from bin.command_line_parser import command_line_parser

calendar_name, date_ini, date_end = command_line_parser()

meals_calendar = CalendarManager(calendar_name)
events = meals_calendar.get_events(date_ini, date_end)

ingredients = parse_meals(events)

print(ingredients)
