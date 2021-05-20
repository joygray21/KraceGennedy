# KraceGennedy

A basic user interface that will check and display the weather forecast for the next 5 days and automate the sending of emails out to staff.

https://www.hindawi.com/journals/tswj/2012/894313/

## How to Run the Application:
1. Create a Mailtrap account and set environment variables with the credentials:
export MAIL_SERVER="smtp.mailtrap.io"
export MAIL_PORT=465
export MAIL_USERNAME="your mailtrap SMTP username"
export MAIL_PASSWORD="your mailtrap SMTP password"
export SECRET_KEY="some random set of characters"

2. Subscribe to the OpenWeather API and set environment variable with your API_KEY 
export API_KEY="your key"

3. Create postgres database and user. Make the user the owner of the database. Set environment variable with the URI using the format:
export DATABASE_URL=postgresql://yourusername:yourpassword@localhost/databasename
3b. Then update the or value in config.py for the URI

4. Run:
$ python -m venv venv 
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt 
$ python run.py

4b. run: python3.9 manage.py db upgrade