import EventCalendar.period as Period
import EventCalendar.event as Event
import datetime, json

def get_json(object):
  return json.loads(
    json.dumps(object, default=lambda o: getattr(o, '__dict__', str(o)))
  )

class Calendar():
    """docstring for Calendar."""

    def __init__(self, startDate = None, defaultPeriodLength = 28,  periods = list(), name = str(), logFile = None):
        super(Calendar, self).__init__()
        if logFile == None:
            self.logFile = open('logs/'+name+'.log', 'a+')
        else:
            self.logFile = logFile
        if not defaultPeriodLength > 0:
            raise ValueError('defaultPeriodLength must be > 0')
        if startDate == None and len(periods) == 0:
            raise ValueError('Supply startDate or not empty periods')
        self.periods = periods.copy()
        self.periods.sort()
        if startDate == None:
            startDate = self.periods[0].dateRange[0]
        self.startDate = startDate
        self.defaultPeriodLength = defaultPeriodLength
        self.name = name
    def addEvent(self, event_):
        if not isinstance(event_, Event.event):
            raise TypeError('event is not EventCalendar.Event.event object')
        if event_.date < self.startDate:
            raise ValueError('event has not valid date')
        success = False
        self.logFile.write(json.dumps(get_json(event_)) + '\n')
        for x in self.periods:
            try:
                x.addEvent(event_)
                success = True
                break
            except ValueError:
                pass
        if not success:
            periodNum = -1
            dateDiff = (event_.date - self.startDate).days
            while dateDiff > 0:
                dateDiff -= self.defaultPeriodLength
                periodNum += 1
            dateRange = [self.startDate + periodNum * datetime.timedelta(days = self.defaultPeriodLength),
                self.startDate + (periodNum + 1) * datetime.timedelta(days = self.defaultPeriodLength)]
            newPeriod = Period.period(dateRange, list())
            newPeriod.addEvent(event_)
            self.periods.append(newPeriod)
            self.periods.sort()
    def findEvent(self, event_):
        res = list()
        for x in self.periods:
            if x.isValid(event_):
                res += x.findEvent(event_)
        return res
    def __str__(self):
        res = 'Calendar on ' + str(self.startDate) + '\n '
        for x in self.periods:
            res += str(x).replace('\n', '\n ') + '\n'
        return res.strip()
