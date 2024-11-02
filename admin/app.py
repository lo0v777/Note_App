from flask import (
    Flask, 
    redirect,
    )
from flask_sqlalchemy  import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Users, Note

import pymysql


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9A68E85B5F0593EDC601435D236CF9B0917405F6012F0F946DDF4F6250485382'

pymysql.install_as_MySQLdb()    


db.init_app(app) 
 

with app.app_context():
    db.create_all()


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(ModelView(Users,db.session))
admin.add_view(ModelView(Note,db.session))


@app.route('/',methods=['GET'])
def admin_panel():
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True,port=5001)


