import os


class Config(object):
    SECRET_KEY='9A68E85B5F0593EDC601435D236CF9B0917405F6012F0F946DDF4F6250485382' 
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:12345678@localhost/db'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False