from WebDeamon.UonetParser import GetTests, user
from WebDeamon.routes import EventCalendar
import datetime

def Uonet(calendar):
    tests = GetTests(user)
    for test in tests:
        date = [int(x) for x in test['date'].split('-')]
        try:
            calendar.addEvent(EventCalendar.Event.event(
                date = datetime.date(date[2], date[1], date[0]),
                name = test['name'],
                author = 'UonetParser',
                time = datetime.time(0, 0)
            ))
        except Exception as e:
            print(e)
    return calendar
