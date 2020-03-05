import EventCalendar.event as Event
import EventCalendar.day as Day

class period():
    """docstring for period."""

    def __init__(self, dateRange, days = list()):
        super(period, self).__init__()
        self.dateRange = dateRange
        self.days = days
    def isValid(self, day_):
        if day_.date == None:
            return True
        return day_.date >= self.dateRange[0] and day_.date <= self.dateRange[1]
    def findEvent(self, event_):
        if isValid(event_):
            res = list()
            for day in self.days:
                for x in day.findEvent(event_):
                    res.append(x)
            return res
        else:
            return list()
    def addEvent(self, event):
        if not self.isValid(event):
            raise ValueError('Event not valid')
        success = False
        for day in self.days:
            if day.date == event.date:
                day.events.append(event)
                success = True
                break
        if not success:
            self.days.append(Day.day(event.date, [event]))
    def __str__(self):
        res = str(self.dateRange[0]) + ' - ' + str(self.dateRange[1]) + '\n '
        for x in self.days:
            res += str(x).replace('\n', '\n ') + '\n'
        return res.strip()
    def __lt__(self, other):
        return self.dateRange[0] < other.dateRange[0]
