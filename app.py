import datetime
import os
from PIL import Image
from db_call import db_call
from flask import Flask, request, render_template, flash, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import timedelta
from data_base import users, db_init, db

app = Flask(__name__)
app.secret_key = "guitarboy06"
app.permanent_session_lifetime = timedelta(minutes=10)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_init(app)


def prof_age(dob):
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) <
                                   (dob.month, dob.day))
    return age


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        u_name = request.form["uname"]
        psd = request.form["psd"]
        result = users.query.filter_by(user_name=u_name).first()
        if result:
            if psd == result.password:
                session["user"] = u_name
                session["pass"] = psd
                return redirect(url_for('profile'))
            else:
                flash("Invalid username or password")
                return render_template("index.html")
        else:
            flash("Username and password is not given")
            return render_template("index.html")
    else:
        return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        flash("you have already registered")
        return redirect(url_for("profile"))

    elif request.method == "POST":
        username = request.form['u_name']
        found_user = users.query.filter_by(user_name=username).first()
        if found_user:
            flash("Username already user")
            return render_template("register.html")
        else:
            name = request.form['f_name'] + " " + request.form['l_name']
            email = request.form['email']
            phone = request.form['phone']
            g_name = request.form['f_g_name'] + " " + request.form['l_g_name']
            address = request.form['address']
            dob = datetime.datetime.strptime(request.form['dob'], '%Y-%m-%d')
            occupation = request.form['occupation']
            psd = request.form['psd']
            pic = request.files['img']
            filename = secure_filename(pic.filename)
            image_name, extension = filename.split(".")
            image_name = username
            img_path = os.path.join("static/profile_pic", image_name + "." + extension)
            a = users(username, psd, name, g_name, email, phone, dob, occupation, address, img_path)
            db.session.add(a)
            db.session.commit()
            image = Image.open(pic)
            image.resize((200, 200))
            image.save(img_path)
            session["user"] = username
            session["pass"] = psd
            return redirect(url_for("profile"))
    else:
        return render_template("register.html")


@app.route("/profile", methods=["POST", "GET"])
def profile():
    if 'user' in session:
        username = session['user']
        prof = db_call(username)
        age = prof_age(prof["dob"])
        return render_template("profile.html", username=username, img=prof["img_path"], name=prof["name"],
                               email=prof["email"],
                               guardian_name=prof["guardian_name"], phone=prof["phone"], address=prof["address"],
                               occupation=prof["occupation"],
                               age=age, dob=prof["dob"])
    else:
        flash("you are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user', None)
        session.pop('psd', None)
        return render_template("logout.html")
    else:
        flash("you are not logged in yet")
        return redirect(url_for("login"))


@app.route("/edit", methods=["POST", "GET"])
def edit():
    if "user" in session:
        if request.method == "POST":
            u_ = session["user"]
            pf = db_call(u_)
            username = request.form["u_name"]
            name = request.form['f_name'] + " " + request.form['l_name']
            email = request.form['email']
            phone = request.form['phone']
            g_name = request.form['f_g_name'] + " " + request.form['l_g_name']
            dob = datetime.datetime.strptime(request.form['dob'], '%Y-%m-%d')
            occupation = request.form['occupation']
            psd = request.form['psd']
            img_path = pf["img_path"]
            address = pf["address"]
            a = users(username, psd, name, g_name, email, phone, dob, occupation, address, img_path)
            db.session.commit()
            session["user"] = username
            session["pass"] = psd
            return redirect(url_for("profile"))
        else:
            username = session["user"]
            prof = db_call(username)
            f_name = prof["name"].split()[0]
            l_name = prof["name"].split()[1]
            f_g_name = prof["guardian_name"].split()[0]
            l_g_name = prof["guardian_name"].split()[1]
            return render_template("edit.html", username=username, f_name=f_name, l_name=l_name, f_g_name=f_g_name,
                                   l_g_name=l_g_name, email=prof["email"], phone=prof["phone"],
                                   occupation=prof["occupation"], dob=prof["dob"])
    else:
        flash("you are not logged in")
        return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
