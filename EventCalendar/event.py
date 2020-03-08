import datetime

class event():
    """docstring for event."""
    def __init__(self, date, time, name, properties = dict(), author = str()):
        super(event, self).__init__()
        if type(time) != datetime.time:
            raise Exception('Time is not datetime.time')
        if not isinstance(date, datetime.date):
            raise Exception('Date is not datetime.date')
        self.date = date
        self.time = time
        self.name = name
        self.properties = properties
        self.author = author
    def __eq__(self, other):
        if not isinstance(other, event):
            return NotImplemented
        return self.time == other.time and self.name == other.name and self.properties == other.properties and self.date == other.date
    def __ne__(self, other):
        if not isinstance(other, event):
            return NotImplemented
        return not self == other
    def __hash__(self):
        return hash((self.time, self.name, self.properties, self.date))
    def __lt__(self, other):
        if self.date == other.date:
            return self.time < other.time
        else:
            return self.date < other.date
    def __str__(self):
        return self.name + ' ' + str(self.time)

class dummyEvent(event):
    """docstring for dummyEvent."""

    def __init__(self, date = None, time = None , name = None , properties = None, author = None):
        self.time = time
        self.name = name
        self.properties = properties
        self.author = author
        self.date = date
    def isEvent(self, other):
        time = self.time in [other.time, None]
        author = self.author in [other.author, None]
        properties = self.properties in [other.properties, None]
        name = self.name in [other.name, None]
        date = self.date in [other.date, None]
        return time and author and properties and name and date
