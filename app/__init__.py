from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
from .config import Config

app = Flask(__name__)

db = SQLAlchemy(app) #connect to db
mail = Mail(app)

app.config.from_object(Config)
from app import views, models