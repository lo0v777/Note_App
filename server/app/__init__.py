from flask import Flask
from app.models import db


app=Flask(__name__,static_folder='./static',template_folder='./templates',static_url_path='/')
app.secret_key = '10BFF217D438D95A7A12954C633EDA48F728D00141D54995E02E5C0AD2F266B7' 
app.config.from_object('app.config.Config')
db.init_app(app)

with app.app_context():
    db.create_all()


from app import routes  


