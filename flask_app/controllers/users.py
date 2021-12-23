from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'id' not in session:
        return render_template("index.html")
    return redirect("/result")

@app.route('/result')
def result():
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': session['id']
    }
    followings = User.get_following_user(data)
    # movies = Movie.get_top5movie(data)
    users = User.get_user_by_id(data)
    top5movie = Movie.get_top5movie(data)
    return render_template("user.html", users=users, followings=followings, top5movie=top5movie)

@app.route('/result/<int:id>')
def result_by_id(id):
    data = {
        'id': id
    }
    followings = User.get_following_user(data)
    # movies = Movie.get_top5movie(data)
    users = User.get_user_by_id(data)
    return render_template("user.html", users=users, followings=followings)

@app.post('/register')
def register():
    if User.is_valid(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "username" : request.form['username'],
            "email" : request.form['email'],
            "password" : pw_hash
        }
        id = User.register(data)
        session['id'] = id
        return redirect("/result")
    return redirect('/')
    
@app.route("/to_edit/<int:id>")
def to_edit_profile(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    return render_template("edit_profile.html", user = User.get_user_by_id(data))

@app.post('/edit/<int:id>')
def edit_profile(id):
    if 'id' not in session:
        return redirect('/')
    data = {
        'id': id,
        "username" : request.form['username'],
        "movie_quote" : request.form['movie_quote'],
    }
    User.edit_profile(data)
    return redirect("/result")

@app.post('/login')
def login():
    user_in_db = User.get_by_email(request.form)

    if not user_in_db:
        flash("Invalid Email/Password",'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Username/Password",'login')
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect("/result")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
