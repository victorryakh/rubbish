from icalendar import Calendar, Event
from datetime import datetime, timedelta
import requests


year = datetime.now().year
cc = 'ru'
api_url = f"https://isdayoff.ru/api/getdata?year={year}&cc={cc}&pre=1&delimeter=%0A&covid=0&sd=0"

def create_all_day_event(cal, title, date):
    event = Event()
    event.add('summary', title)
    event.add('dtstart', date)
    event.add('dtend', date + timedelta(days=1))
    event.add('dtstamp', datetime.now())
    cal.add_component(event)

# Create a calendar
cal = Calendar()
cal.add('prodid', '-//My Calendar//example.com//')
cal.add('version', '2.0')

# Iterate over the is_day_off list and create events
def get_list(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return [int(line) for line in response.text.splitlines()]
    else:
        raise requests.exceptions.ConnectionError

for i, is_day_off in enumerate(get_list(api_url)):
    event_date = datetime(year, 1, 1) + timedelta(days=i)
    if is_day_off == 0:
        create_all_day_event(cal, "Официальный рабочий день 💼", event_date)
    if is_day_off == 1:
        create_all_day_event(cal, "Официальный нерабочий день 🛋️", event_date)
    if is_day_off == 2:
        create_all_day_event(cal, "Официальный сокращённый день 🕔", event_date)
# Save calendar to a file
with open('day_off_calendar.ics', 'wb') as f:
    f.write(cal.to_ical())