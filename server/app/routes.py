from app.models import Users, db, Note
from flask import render_template, request, session, flash, redirect, url_for, jsonify
from app import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session: 
            return redirect(url_for('login'))  
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  
    return wrapper


@app.route("/", methods=["GET","POST"])
def login():
    if request.method =="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Users.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id #####
            return render_template('main.html', username = username)
        else:
            return render_template("login.html",  message = "The user does not exist")
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        existing_user = Users.query.filter((Users.username == username) | (Users.password == password)).first()
        if existing_user:
            return render_template("register.html", message="User already exists")
        if password == password2:
            new_user = Users(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", LogIn="Your create account successfully, please login")
        else:
            return render_template("register.html", message = "Please, input correct data")

    return render_template("register.html")


@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route("/notes", methods = ["GET", "POST"])
@login_required
def main():
    user_id = session.get('user_id')
    
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        new_note = Note(title=title, content=content, user_id=user_id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('main'))
    
    user_notes = Note.query.filter_by(user_id=user_id).all()
    return render_template("main.html", notes=user_notes)
    # return render_template("main.html")

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for("login"))



@app.route("/get_notes", methods=["GET"])
@login_required
def get_notes():
    user_id = session.get("user_id")
    user_notes = Note.query.filter_by(user_id=user_id).all()
    notes = [{"title": note.title, "content": note.content} for note in user_notes]
    return jsonify(notes)
