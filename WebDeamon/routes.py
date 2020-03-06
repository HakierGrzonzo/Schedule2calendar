from WebDeamon import app
from flask import request, render_template, abort
import EventCalendar
import datetime

calendars = list()

@app.route('/')
@app.route('/index')
def index():
    global calendars
    error = None
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
    calendar_return = list([{'name': x.name, 'startDate': x.startDate,
        'url': '/calendar/'+x.name} for x in calendars])
    if len(calendar_return) == 0:
        calendar_return = None
    return render_template('index.html', calendars = calendar_return, error = error)

@app.route('/calendar/<calendarName>')
def calendarDisplayer(calendarName):
    global calendars
    calendar = None
    for x in calendars:
        if calendarName == x.name:
            calendar = x
            break
    if calendar == None:
        abort(404)
