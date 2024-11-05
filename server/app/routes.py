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
    return render_template("main.html", notes=user_notes)  


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
