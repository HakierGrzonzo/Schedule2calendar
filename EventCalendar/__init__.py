from EventCalendar import event as Event
from EventCalendar import period as Period
from EventCalendar import day as Day
from EventCalendar import calendar as Calendar
import json, datetime
def get_json(object):
  return json.loads(
    json.dumps(object, default=lambda o: getattr(o, '__dict__', str(o)))
  )

def load_from_dict(data):
    return Calendar.Calendar(
        startDate = data['startDate'],
        defaultPeriodLength = data['defaultPeriodLength'],
        periods = list(
            [Period.period(
                dateRange = list([
                    datetime.date.fromisoformat(x)
                    for x in period['dateRange']
                ]),
                days = list([
                    Day.day(
                        date = datetime.date.fromisoformat(day['date']),
                        events = list([
                            Event.event(
                                date = datetime.date.fromisoformat(event['date']),
                                time = datetime.time.fromisoformat(event['time']),
                                name = event['name'],
                                properties = event['properties'],
                                author = event['author']
                            )
                            for event in day['events']
                        ])
                    )
                    for day in period['days']
                ])
            )
            for period in data['periods']
        ])
     )