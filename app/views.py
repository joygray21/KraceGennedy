from app import app, db, mail
from flask import render_template, request, redirect, url_for
from flask_mail import Message
import requests, json #python libraries
from datetime import date 
from .models import Worker #, EmailHistory

###
# Routes
###

@app.route('/')
def home():
    """Render website's home page."""
    # initializing values
    rainyTmrw =  False
    rainyAnyDay = False
    rainyDays = ''

    #initializing 

    # get 5 day forecast
    data = get_forecast()
    
    # Send appropriate emails
    # ideally: check db to see if emails were already sent for the day. If yes, don't resend, otherwise, send
    for city in data:
        for day in range(1,6):
            day_fore = getDayfromCityForecasts(data[city], day)
            print(data[city])
            print(day_fore)
            if isRainy(getRainfromDayForecast(day_fore)):
                if day == 1 :
                    rainyTmrw = True

                rainyAnyDay = True       
                rainyDays += (getDatefromDayForecast(day_fore)) + "; "
                    
        if rainyTmrw:
            subject = 'Rainy Day Tomorrow'
            r_emails = getWorkersEmails(getAffectedWorkers(city))
            body = "Good day all.\n"+ \
                    "Tomorrow {0} will be a rainy day. \n".format((rainyDays.split(';'))[0]) + \
                    "Hence, you will only work for four (4) hours tomorrow instead of the usual eight (8)."
            if r_emails != []:
                sendEmail(subject, r_emails, body)
        else:
            subject = 'Sunny Day Tomorrow'
            r_emails = getWorkersEmails(getAllWorkers(city))
            body = "Good day all.\n"+ \
                    "Tomorrow {0} will be a sunny day. \n".format(getDayfromCityForecasts(data[city], 1)) + \
                    "Hence, you will work the usual eight (8) hours."
            if r_emails != []:
                sendEmail(subject, r_emails, body)
            

    if rainyAnyDay:
        subject = 'Rain During the Next 5 Days'
        r_emails = getWorkersEmails(getITWorkers(city))
        body = "Good day all.\n"+ \
                "The following day(s) will be rainy: {0} \n".format(rainyDays[0]) + \
                "Hence, on those days you will only work in office."
        if r_emails != []:
                sendEmail(subject, r_emails, body)


    return render_template('home.html', data = data)

# API Route
@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    daysOfTheWeek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

    cities = ['Montego Bay', 'Kingston'] #for scalability, retrieve unique cities from db (next version)
    forecasts = {} #dictionary with each city and a list of its forecasts for the next 5 days
    
    for city in cities:
        #first get city coordinates
        #get weather of city which contains the coordinates using Weather API
        coord_req = requests.get('http://api.openweathermap.org/data/2.5/weather?q={city}&appid={APIKey}'.format(city=city, APIKey=app.config['API_KEY']))
        
        #convert the data to a python object (dict) with json.loads
        coord_content = json.loads(coord_req.content)
        
        #get coordinates
        lon = coord_content['coord']['lon']
        lat = coord_content['coord']['lat']
        
        
        #use coordinates to get forecast for city using One Call API
        #exclude parts of response except daily         ---X and alerts X (next version)
        #get temp values in Celsius - metric units
        fore_req = requests.get('http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&units={units}&appid={APIKey}'.format(lat=lat, lon=lon, exclude='current,minutely,hourly,alerts', units=app.config['UNITS'], APIKey=app.config['API_KEY']))
        
        
        #convert the data to a python object getting only data for the next five days 
        fore_results = json.loads(fore_req.content)['daily'][1:6]

        #prepare storage for that city's forecasts 
        forecasts[city] = []
        
        for forecast in fore_results: #for each day 
            #convert timestamp
            fore_date = date.fromtimestamp(forecast['dt'])
            day = fore_date.day     #day of the month
            weekdayNum = fore_date.weekday() 

            impData = [ #data needed 
                #fore_date,
                day, 
                daysOfTheWeek[weekdayNum], #get weekday name
                forecast['weather'][0]['description'], #weather description
                forecast['pop'], #probability of rain
                int(forecast['rain']),   #mm of rain
                forecast['temp']['min'], #minimum temperature of the day
                forecast['temp']['max'] 
            ]

            # impData = { #data needed 
            #     #fore_date,
            #     'day':day, 
            #     'weekday':daysOfTheWeek[weekdayNum], #get weekday name
            #     'desc':forecast['weather'][0]['description'], #weather description
            #     'pop':forecast['pop'], #probability of rain
            #     'rain':forecast['rain'],   #mm of rain
            #     'min':forecast['temp']['min'], #minimum temperature of the day
            #     'max':forecast['temp']['max'] 
            # }
            
            #add data to the forecasts dictionary
            forecasts[city].append(impData) 

    #X display forecast information for the next five days X
    #return render_template('home.html', data = forecasts) 

    #return forecast information for the next five days
    return forecasts


###
# Other Functions 
###

# Getters for Forecast
def getDayfromCityForecasts(cityForecasts, day):
    """ Takes in the 5day forecasts for a city and returns the data for the day specified"""

    if day not in range (1,6):
        print ("Day value must be from 1 to 5")
    else:
        day-=1
        return cityForecasts[day]

def getDatefromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the string 'Weekday_name, Day_of_the_month' """
    return "{1}, {2}".format(dayForecast[1], dayForecast[0])

def getDescfromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the description' """
    return dayForecast[3]
    
def getPopfromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the probability of rain' """
    return dayForecast[4]

def getRainfromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the level of rain' """
    return dayForecast[5]

def getMinfromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the minimum temperature' """
    return dayForecast[6]

def getMaxfromDayForecast(dayForecast):
    """ Takes in a day's forecast and returns the maximum temperature' """
    return dayForecast[7]


#
def isRainy(rain):
    return int(rain) >= app.config['RAINY_DAY_DEF']


# Get Worker Data from Database
def getAllWorkers(city):
    return Worker.query.all()

def getAffectedWorkers(city):
    return Worker.query.filter_by(city=city).all()

def getITWorkers(city):
    return Worker.query.filter_by(role='IT').all()


def getWorkersEmails(workers):
    emails = []
    if workers is not None:
        for worker in workers:
            emails.append(worker.email)
    
    return emails
    


# Send Email
def sendEmail(subject, r_emails, body):
    msg = Message(subject, sender=(app.config['BOSS_NAME'], app.config['BOSS_EMAIL']), recipients = r_emails)
    msg.body = body
    mail.send(msg)    

    return 



### run statement
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
