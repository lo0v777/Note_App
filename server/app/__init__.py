from flask import Flask
from app.models import db
from flask_mail import Mail
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

app=Flask(__name__,static_folder='./static',template_folder='./templates',static_url_path='/')
app.secret_key = '10BFF217D438D95A7A12954C633EDA48F728D00141D54995E02E5C0AD2F266B7' 
app.config.from_object('app.config.Config')
db.init_app(app)


engine = sqlalchemy.create_engine('mysql+pymysql://username:password@db_name')

with engine.connect() as connection:
    connection.execute(sqlalchemy.text("CREATE DATABASE IF NOT EXISTS db"))
    
    connection.execute(sqlalchemy.text("USE db"))
    
    
engine = sqlalchemy.create_engine('mysql+pymysql://username:password@db_name/db')


with engine.connect() as connection:
    result = connection.execute(sqlalchemy.text("SELECT DATABASE()"))
    if result:
        print("db exiting")
    else:
        print("db not existing")  


mail = Mail(app)

with app.app_context():
    db.create_all()

from app import routes  



