from flask import (
    Flask, 
    redirect
    )
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Note
from flask_login import current_user
import pymysql, sqlalchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@db_name/db'  

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9A68E85B5F0593EDC601435D236CF9B0917405F6012F0F946DDF4F6250485382'

pymysql.install_as_MySQLdb()    
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
 

with app.app_context():
    db.create_all()

class NoteModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if is_created:  
            if current_user.is_authenticated:  
                model.user_id = current_user.id 
            else:
                raise ValueError("User not auth!")
        return super().on_model_change(form, model, is_created)

admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(Users,db.session))
admin.add_view(NoteModelView(Note, db.session))  

@app.route('/',methods=['GET'])
def admin_panel():
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0", port=5001)


