import datetime
import EventCalendar.event as event

class day():
    """docstring for day."""

    def __init__(self, date, events = list()):
        super(day, self).__init__()
        if not isinstance(date, datetime.date):
            raise Exception('date in not datetime.date')
        self.date = date
        self.events = events.copy()
    def addEvent(self, event_):
        if not isinstance(event_, event.event):
            raise Exception('Event is not calendar.event.event')
        if event_.date != self.date:
            raise Exception('Event is not valid for this day')
        self.events.append(event_)
        self.events.sort()
    def findEvent(self, toFind):
        res = list()
        for event_ in self.events:
            if isinstance(toFind, event.dummyEvent):
                if toFind.isEvent(event_):
                    res.append(event_)
            else:
                if toFind == event_:
                    res.append(event_)
        return res
    def __str__(self):
        res = str(self.date) +'\n'
        for x in self.events:
            res += ' |' + str(x) +'\n'
        return res.strip()
    def __lt__(self, other):
        return self.date < other.date
