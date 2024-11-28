import os
from app import app

class Config(object):
    SECRET_KEY='9A68E85B5F0593EDC601435D236CF9B0917405F6012F0F946DDF4F6250485382' 
    # SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:12345678@localhost/db'   
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:12345678@db/db'   

    SQLALCHEMY_TRACK_MODIFICATIONS = False  

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL= True
    MAIL_USERNAME = 'lo0v777@mail.ru'  
    MAIL_PASSWORD = '47TPJWQLKfWbcnPbiWE0'#qweqweewq


    

    