import argparse

def command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date_ini')
    parser.add_argument('--date_end')
    parser.add_argument('--calendar_name')
    args = parser.parse_args()
    arguments = args.__dict__
    return arguments['calendar_name'], arguments['date_ini'], arguments['date_end']
