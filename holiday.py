import sys
import re
import pathlib
import datetime


HOL_DATE_FORMAT = "%Y/%m/%d"
ICS_DATE_FORMAT = "%Y%m%d"

INPUT_BUSY_STATUS = "OOF"


def print_calendar(outfilename, section, event_lines):
    with open(outfilename, "wt") as outfile:
        outfile.write("BEGIN:VCALENDAR\n")
        outfile.write("VERSION:2.0\n")
        outfile.write("PRODID:-//scastria/ics//EN\n")
        for line in event_lines:
            line = line.strip()
            event_tokens = line.split(",")
            event_name = event_tokens[0]
            event_date = event_tokens[1]
            print_event(outfile, section, event_name, event_date)
        outfile.write("END:VCALENDAR\n")


def print_event(outfile, section, name, date):
    dstart = datetime.datetime.strptime(date, HOL_DATE_FORMAT)
    dend = dstart + datetime.timedelta(days=1)
    outfile.write("BEGIN:VEVENT\n")
    outfile.write(f"SUMMARY:{name} ({section})\n")
    outfile.write(f"DTSTART;VALUE=DATE:{dstart.strftime(ICS_DATE_FORMAT)}\n")
    outfile.write(f"DTEND;VALUE=DATE:{dend.strftime(ICS_DATE_FORMAT)}\n")
    outfile.write(f"X-MICROSOFT-CDO-BUSYSTATUS:{INPUT_BUSY_STATUS}\n")
    outfile.write("END:VEVENT\n")


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
    print_calendar(f"{infile_path.stem}.ics", section, input_lines[1:])


if __name__ == '__main__':
    main()
