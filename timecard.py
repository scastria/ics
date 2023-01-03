import sys
import re
import pathlib
import datetime


HOL_DATE_FORMAT = "%Y/%m/%d"
ICS_DATE_FORMAT = "%Y%m%d"

INPUT_TIMEZONE = "America/Los_Angeles"
INPUT_TIME_EMPLOYEE_START = "083000"
INPUT_TIME_EMPLOYEE_STOP = "090000"
INPUT_TIME_SUPERVISOR_START = "113000"
INPUT_TIME_SUPERVISOR_STOP = "120000"
INPUT_BUSY_STATUS = "FREE"
INPUT_ALARM = "-PT23H30M"


def print_calendar(outfilename, section, event_lines, is_supervisor):
    with open(outfilename, "wt") as outfile:
        outfile.write("BEGIN:VCALENDAR\n")
        outfile.write("VERSION:2.0\n")
        outfile.write("PRODID:-//scastria/ics//EN\n")
        for line in event_lines:
            line = line.strip()
            event_tokens = line.split(",")
            event_name = event_tokens[0]
            event_date = event_tokens[1]
            print_event(outfile, section, event_name, event_date, is_supervisor)
        outfile.write("END:VCALENDAR\n")


def print_event(outfile, section, name, date, is_supervisor):
    time_start = INPUT_TIME_SUPERVISOR_START if is_supervisor else INPUT_TIME_EMPLOYEE_START
    time_stop = INPUT_TIME_SUPERVISOR_STOP if is_supervisor else INPUT_TIME_EMPLOYEE_STOP
    d = datetime.datetime.strptime(date, HOL_DATE_FORMAT)
    outfile.write("BEGIN:VEVENT\n")
    outfile.write(f"SUMMARY:{name} ({section})\n")
    outfile.write(f"DTSTART;TZID={INPUT_TIMEZONE}:{d.strftime(ICS_DATE_FORMAT)}T{time_start}\n")
    outfile.write(f"DTEND;TZID={INPUT_TIMEZONE}:{d.strftime(ICS_DATE_FORMAT)}T{time_stop}\n")
    outfile.write(f"X-MICROSOFT-CDO-BUSYSTATUS:{INPUT_BUSY_STATUS}\n")
    print_alarm(outfile)
    outfile.write("END:VEVENT\n")


def print_alarm(outfile):
    outfile.write("BEGIN:VALARM\n")
    outfile.write("DESCRIPTION:REMINDER\n")
    outfile.write(f"TRIGGER;RELATED=START:{INPUT_ALARM}\n")
    outfile.write("ACTION:DISPLAY\n")
    outfile.write("END:VALARM\n")


def main():
    infilename = sys.argv[1]
    infile_path = pathlib.Path(infilename)
    with open(infilename, "rt") as infile:
        input_lines = infile.readlines()
    section_header = r"\[(?P<section>.*)\](?P<event_count>\d+)"
    section_pattern = re.compile(section_header)
    match = section_pattern.match(input_lines[0])
    section = match.group("section")
    event_count = int(match.group("event_count"))
    if len(input_lines) != event_count + 1:
        raise Exception(f"Number of events {len(input_lines) - 1} does not match section header {event_count}")
    print_calendar(f"{infile_path.stem}_employee.ics", section, input_lines[1:], False)
    print_calendar(f"{infile_path.stem}_supervisor.ics", section, input_lines[1:], True)


if __name__ == '__main__':
    main()
