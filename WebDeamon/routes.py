from WebDeamon import app
from flask import request, render_template, abort
import EventCalendar
import datetime, json, os

calendars = list()

@app.route('/')
@app.route('/index')
def index():
    global calendars
    error = None
    # if new calendar was requested -> try to create it
    try:
        newCalendarName = request.args.get('calendarName')
        if newCalendarName in [x.name for x in calendars]:
            error = "Calendar already in database"
        elif not (newCalendarName == None or newCalendarName.strip() == str()):
            calendars.append(EventCalendar.Calendar.Calendar(
                startDate = datetime.date.today(),
                name = newCalendarName
            ))
    except Exception as e:
        print(e)
    # Create list of calendars for the page
    calendar_return = list([{'name': x.name, 'startDate': x.startDate,
        'url': '/calendar/'+x.name} for x in calendars])
    if len(calendar_return) == 0:
        calendar_return = None
    return render_template('index.html', calendars = calendar_return, error = error)

@app.route('/calendar/<calendarName>')
def calendarDisplayer(calendarName):
    global calendars
    error = None
    calendar = None
    # find requested calendar by name
    for x in calendars:
        if calendarName == x.name:
            calendar = x
            break
    # on faliure -> 404
    if calendar == None:
        abort(404)
    #Extract data for new event from query:
    try:
        data = request.args
        timeArr = data.get('eventTime').split(':')
        event = EventCalendar.Event.event(
            name = data.get('eventName'),
            date = datetime.date.fromisoformat(data.get('eventDate')),
            time = datetime.time(int(timeArr[0]), int(timeArr[1])),
            author = 'web-ui'
        )
        if len(calendar.findEvent(event)) == 0:
            calendar.addEvent(event)
        else:
            error = 'This event is already in this calendar.'
    except KeyError:
        pass
    except AttributeError:
        pass
    # Create list of days from the calendar, and convert them to json
    dayArray = list()
    for period in calendar.periods:
        for day in period.days:
            dayArray.append(day)
    dayArray = [EventCalendar.get_json(x) for x in dayArray]
    # remove seconds from time
    for i in range(len(dayArray)):
        for j in range(len(dayArray[i]['events'])):
            dayArray[i]['events'][j]['time'] = dayArray[i]['events'][j]['time'][:len(dayArray[i]['events'][j]['time']) - 3]
    # sync the local database
    localSync()
    return render_template('calendar.html', name = calendar.name, days = dayArray, minDate = calendar.startDate.isoformat(), error = error)

@app.route('/sync/local')
def localSync():
    """save the calendars, and load them from files"""
    global calendars
    for x in calendars:
        EventCalendar.save_calendar(x)
    calendars = list()
    for dirpath, dirnames, filenames in os.walk('calendars/'):
        for x in filenames:
            with open(os.path.join(dirpath, x), 'r') as f:
                calendars.append(EventCalendar.load_from_dict(json.loads(f.read())))
    return "success"
