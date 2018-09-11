"""
    Wikipedia Years

    Created by Eric Kong, September 2018
    All rights reserved.
"""

import datetime
import requests

MONTH_NAMES = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
               'May': 5, 'June': 6, 'July': 7, 'August': 8,
               'September': 9, 'October': 10, 'November': 11, 'December': 12}

"""
    Event class.

    Stores the two datetime.date objects bounding the event
    and a string describing the event.
"""
class Event(object):
    def __init__(self, begin_date, end_date, string):
        self.begin_date = begin_date
        self.end_date = end_date
        self.string = string
    def __str__(self):
        if self.begin_date == self.end_date:
            return self.begin_date.strftime("%B %d, %Y") + ": " + self.string
        else:
            return self.begin_date.strftime("%B %d, %Y") + " to " + self.end_date.strftime("%B %d, %Y") + ": " + self.string
    

"""
    get_page(page_name)

    Retrieves a raw-text-format page from Wikipedia,
    with the name page_name. If the response code is not 200 OK,
    return an empty string.
"""
def get_page(page_name):
    URL = "https://en.wikipedia.org/wiki/%s" % page_name
    PARAMS = {
        'action': 'raw'
        }
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code == 200:
        return r.text
    else:
        return ""

"""
    get_events(year)

    Returns a list of Event objects which represent the
    events which transpired in the year. If year is not a reasonable
    input, return an empty list.
"""
def get_events(year):
    text = get_page(str(year))
    if not text:
        return []
    lines = text.split('\n')
    events = []
    section = "" # Events, Births, Deaths
    month_day = "" # Keep track of current month and day in loop.
    for line in lines:
        if len(line) > 2 and line[0:2] == "==" and line[2] != "=": # Section header.
            section = line.strip('= ')
        elif section == "Events":
            rendered = render_text(line)
            if len(rendered) > 1 and rendered[0] == "*":
                if rendered[1] == "*": # Line begins with **.
                    month, day = month_day.split(' ')
                    month = MONTH_NAMES[month]
                    day = int(day)
                    date = datetime.date(year, month, day)
                    string = rendered[2:].strip(' ')
                    events.append(Event(date, date, string))
                else: # Line begins with *.
                    parts = rendered[1:].split('–', 2) # en dash, split at most twice
                    if len(parts) == 1:
                        stripped_part = parts[0].strip(' ')
                        if looks_like_month_day(stripped_part):
                            month_day = stripped_part
                    elif len(parts) == 2:
                        stripped_part = parts[0].strip(' ')
                        if looks_like_month_day(stripped_part):
                            month_day = stripped_part
                            month, day = month_day.split(' ')
                            month = MONTH_NAMES[month]
                            day = int(day)
                            date = datetime.date(year, month, day)
                            string = parts[1].strip(' ')
                            events.append(Event(date, date, string))
                    elif len(parts) == 3:
                        begin_part = parts[0].strip(' ')
                        end_part = parts[1].strip(' ')
                        if looks_like_month_day(begin_part):
                            bmonth, bday = begin_part.split(' ')
                            bmonth = MONTH_NAMES[bmonth]
                            bday = int(bday)
                            bdate = datetime.date(year, bmonth, bday)
                            if looks_like_month_day(end_part):
                                emonth, eday = end_part.split(' ')
                                emonth = MONTH_NAMES[emonth]
                                eday = int(eday)
                                edate = datetime.date(year, emonth, eday)
                                string = parts[2].strip(' ')
                                events.append(Event(bdate, edate, string))
                            if looks_like_day(end_part):
                                emonth = bmonth
                                eday = int(end_part)
                                edate = datetime.date(year, emonth, eday)
                                string = parts[2].strip(' ')
                                events.append(Event(bdate, edate, string))
                            else:
                                parts = rendered[1:].split('–', 1)
                                stripped_part = parts[0].strip(' ')
                                if looks_like_month_day(stripped_part):
                                    month_day = stripped_part
                                    month, day = month_day.split(' ')
                                    month = MONTH_NAMES[month]
                                    day = int(day)
                                    date = datetime.date(year, month, day)
                                    string = parts[1].strip(' ')
                                    events.append(Event(date, date, string))
##        elif section == "Births":
##            rendered = render_text(line)
##            if len(rendered) > 1 and rendered[0] == "*":
##                if rendered[1] == "*": # Line begins with **.
##                    month, day = month_day.split(' ')
##                    month = MONTH_NAMES[month]
##                    day = int(day)
##                    date = datetime.date(year, month, day)
##                    string = "Birth of " + rendered[2:].strip(' ') + "."
##                    events.append(Event(date, date, string))
##                else: # Line begins with *.
##                    parts = rendered[1:].split('–', 2) # en dash, split at most twice
##                    if len(parts) == 1:
##                        stripped_part = parts[0].strip(' ')
##                        if looks_like_month_day(stripped_part):
##                            month_day = stripped_part
##                    elif len(parts) == 2:
##                        stripped_part = parts[0].strip(' ')
##                        if looks_like_month_day(stripped_part):
##                            month_day = stripped_part
##                            month, day = month_day.split(' ')
##                            month = MONTH_NAMES[month]
##                            day = int(day)
##                            date = datetime.date(year, month, day)
##                            string = "Birth of " + parts[1].strip(' ') + "."
##                            events.append(Event(date, date, string))
##        elif section == "Deaths":
##            rendered = render_text(line)
##            if len(rendered) > 1 and rendered[0] == "*":
##                if rendered[1] == "*": # Line begins with **.
##                    month, day = month_day.split(' ')
##                    month = MONTH_NAMES[month]
##                    day = int(day)
##                    date = datetime.date(year, month, day)
##                    string = "Death of " + rendered[2:].strip(' ') + "."
##                    events.append(Event(date, date, string))
##                else: # Line begins with *.
##                    parts = rendered[1:].split('–', 2) # en dash, split at most twice
##                    if len(parts) == 1:
##                        stripped_part = parts[0].strip(' ')
##                        if looks_like_month_day(stripped_part):
##                            month_day = stripped_part
##                    elif len(parts) == 2:
##                        stripped_part = parts[0].strip(' ')
##                        if looks_like_month_day(stripped_part):
##                            month_day = stripped_part
##                            month, day = month_day.split(' ')
##                            month = MONTH_NAMES[month]
##                            day = int(day)
##                            date = datetime.date(year, month, day)
##                            string = "Death of " + parts[1].strip(' ') + "."
##                            events.append(Event(date, date, string))
##    events = sorted(events, key=lambda event: event.begin_date)
    return events

"""
    looks_like_month_day(text)

    Returns true if text is a date formatted like March 15 or August 4,
    false otherwise.
"""

def looks_like_month_day(text):
    words = text.strip(' ').split(' ')
    if len(words) == 2 and words[0] in MONTH_NAMES:
        try:
            num = int(words[1])
            return num >= 1 and num <= 31
        except ValueError:
            return False
    else:
        return False

"""
    looks_like_day(text)

    Returns true if text is a number in the range [1, 31], inclusive.
"""
def looks_like_day(text):
    try:
        num = int(text.strip(' '))
        return num >= 1 and num <= 31
    except ValueError:
        return False

"""
    render_text(text)

    Remove HTML tags and return the rendered Wikipedia markdown, excluding references.
"""
def render_text(text):
    rendered_text = ""
    in_hyperlink = False
    in_reference = False
    hyperlink_text = ""
    i = 0
    while i < len(text):
        if len(text) - i > 1 and text[i:i+2] == '[[':
            in_hyperlink = True
            i += 2
        elif len(text) - i > 1 and text[i:i+2] == ']]':
            in_hyperlink = False
            rendered_text += hyperlink_text
            hyperlink_text = ""
            i += 2
        elif len(text) - i > 1 and text[i:i+2] == '{{':
            i += 2
        elif len(text) - i > 1 and text[i:i+2] == '}}':
            i += 2
        elif in_hyperlink and text[i] == '|':
            hyperlink_text = ""
            i += 1
        elif len(text) - i > 3 and text[i:i+4] == '<ref':
            in_reference = True
            i += 4
        elif len(text) - i > 4 and text[i:i+5] == '/ref>':
            in_reference = False   
            i += 5
        elif len(text) - i > 6 and text[i:i+7] == '&ndash;':
            rendered_text += '–' # en dash
            i += 7
        else:
            if in_reference:
                pass
            elif in_hyperlink:
                hyperlink_text += text[i]
            else:
                rendered_text += text[i]
            i += 1 
    return rendered_text

"""
    find_events_on(date)

    Returns a list of Events which occurred, or were in progress,
    on the date. date is a datetime.date object.
"""
def find_events_on(date):
    year_events = get_events(date.year)
    events = []
    for event in year_events:
        if event.begin_date <= date and event.end_date >= date:
            events.append(event)
    return events

"""
    find_events_around(date, radius)

    Returns a list of Events which occurred, or were in progress,
    on the date, or radius days before or after.
    date is a datetime.date object. radius is an integer.
"""
def find_events_around(date, radius=14):
    begin_date = date - datetime.timedelta(days=radius)
    end_date = date + datetime.timedelta(days=radius)
    year_events = get_events(begin_date.year)
    if end_date.year != begin_date.year:
        year_events.extend(get_events(end_date.year))
    events = []
    for event in year_events:
        if event.begin_date <= end_date and event.end_date >= begin_date:
            before_events.append(event)
    return events

"""
    find_events_on_and_around(date, radius)

    Returns a tuple of three lists of Events.
    The first list contains Events directly preceding the date.
    The second list contains Events on the date.
    The third list contains Events directly following the date.
    The radius controls how many days before or after the date
    we should find Events.
"""

def find_events_on_and_around(date, radius=14):
    begin_date = date - datetime.timedelta(days=radius)
    end_date = date + datetime.timedelta(days=radius)
    year_events = get_events(begin_date.year)
    if end_date.year != begin_date.year:
        year_events.extend(get_events(end_date.year))
    before_events = []
    events = []
    after_events = []
    for event in year_events:
        if event.begin_date <= date and event.end_date >= date:
            events.append(event)
        elif event.begin_date < date and event.end_date >= begin_date:
            before_events.append(event)
        elif event.begin_date <= end_date and event.end_date > date:
            after_events.append(event)
    return (before_events, events, after_events)
