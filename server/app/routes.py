from app.models import Users, db, Note
from flask import render_template, request, session, flash, redirect, url_for, jsonify

from app import app, db, mail
from flask_mail import Message

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
            session['user_id'] = user.id
            return redirect(url_for('main')) 
        else:
            return render_template("login.html",  message = "The user does not exist")
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        email = request.form.get("email")
        existing_user = Users.query.filter((Users.username == username) | (Users.password == password)).first()
        if existing_user:
            return render_template("register.html", message="User already exists")
        if password == password2:
            new_user = Users(username=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html", LogIn="Your create account successfully, please login")
        else:
            return render_template("register.html", message = "Please, input correct data")

    return render_template("register.html")

@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = Users.query.filter_by(email=email).first()
        cur_user = user.username
        if cur_user:
            send_reset_email(user)
            flash("An email has been sent with instructions to reset your password.", "info")
            return render_template("login.html", LogIn = "Check your email")
        else:
            flash("No account found with that email.", "warning")
    return render_template("forgot_password.html")

def send_reset_email(user):
    token = user.generate_reset_token()
    msg = Message('Password Reset Request',
                  sender='lo0v777@mail.ru',    
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    user = Users.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("forgot_password"))
    if request.method == "POST":
        password = request.form.get("password")
        if password:
            user.password = password  
            db.session.commit()
            return render_template("login.html", LogIn = "The password has been successfully updated ")
        else:
            pass
    return render_template("reset_token.html", token=token)

@app.route("/notes", methods=["GET", "POST"])
@login_required
def main():
    user_id = session.get('user_id')
    if request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        if title and content:
            new_note = Note(title=title, content=content, user_id=user_id)
            db.session.add(new_note)
            db.session.commit()
            return jsonify({"success": True}), 201 
        else:
            return jsonify({"success": False, "message": "Invalid data"}), 400
    user_notes = Note.query.filter_by(user_id=user_id).all()
    username = Users.query.get(user_id).username
    return render_template("main.html", notes=user_notes, username=username)  

@app.route("/update_note/<int:note_id>", methods=["POST"])
@login_required
def update_note(note_id):
    note = Note.query.get(note_id)
    if note and note.user_id == session.get('user_id'):
        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        if title and content:
            note.title = title
            note.content = content
            db.session.commit()
            return jsonify({"success": True}), 200  
        else:
            return jsonify({"success": False, "message": "Invalid data"}), 400
    return jsonify({"success": False, "message": "Note not found"}), 404

@app.route("/delete_note/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True}), 200
    return jsonify({"success": False, "message": "Note not found"}), 404

@app.route('/delete_all_notes', methods=['DELETE'])
def delete_all_notes():
    db.session.query(Note).delete() 
    db.session.commit()
    return jsonify({"success": True})

@app.route("/logout")
def logout():   
    session.pop('user_id', None)
    return redirect(url_for("login"))





###to check nginx
@app.route("/check")
def check():
    return str(request.headers)