import os
from app import app

class Config(object):
    SECRET_KEY='9A68E85B5F0593EDC601435D236CF9B0917405F6012F0F946DDF4F6250485382' 
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://username:password@db_name/db'   

    SQLALCHEMY_TRACK_MODIFICATIONS = False  

    MAIL_SERVER = '*****'
    MAIL_PORT = 1111
    MAIL_USE_SSL= True
    MAIL_USERNAME = '*****************'  
    MAIL_PASSWORD = '*****************'


    

    