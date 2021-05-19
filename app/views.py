from app import app
from flask import render_template, request, redirect, url_for
import requests #python library

###
# Routes
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/api/forecast', methods=['GET'])
def get_forecast():
    cities = ['Montego Bay', 'Kingston'] #for scalability, retrieve unique cities from db
    forecasts = {} #dictionary with each city and a list of its forecasts for the next 5 days
    
    for city in cities:
        req = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={APIKey}'.format(city=city, APIKey=app.config['API_KEY'])) 
        c = req.content
        #forecasts[city] = 
    
    return render_template('home.html', data = c)


### run statement
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
