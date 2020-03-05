import EventCalendar, datetime, json
"""
calendar = EventCalendar.Calendar.Calendar(datetime.date.today())
event = EventCalendar.Event.event(datetime.date.today(), datetime.time(15, 20), 'test')
calendar.addEvent(event)
event = EventCalendar.Event.event(datetime.date.today(), datetime.time(16, 20), 'test3')
calendar.addEvent(event)
event = EventCalendar.Event.event(datetime.date.today() + datetime.timedelta(days = 30),
    datetime.time(16, 30), 'test2')
calendar.addEvent(event)
"""
with open('debug.json') as f:
    data = json.loads(f.read())
calendar = EventCalendar.load_from_dict(data)
print(calendar)
