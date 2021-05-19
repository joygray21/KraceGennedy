from app import app
from flask import render_template, request, redirect, url_for
import requests, json #python libraries
from datetime import date 

###
# Routes
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

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
            day = fore_date.day
            weekdayNum = fore_date.weekday() 

            impData = [ #data needed 
                day, 
                daysOfTheWeek[weekdayNum], #get weekday name
                forecast['weather'][0]['description'], #weather description
                forecast['temp']['min'], #minimum temperature of the day
                forecast['temp']['max'] 
            ]

            #add data to the forecasts dictionary
            forecasts[city].append(impData) 

            
    #display forecast information for the next five days
    return render_template('home.html', data = forecasts) 


### run statement
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
