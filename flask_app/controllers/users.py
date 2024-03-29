from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.follow import Follow
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
bcrypt = Bcrypt(app)


@app.route('/mywatchlist')
def index():
    if 'id' not in session:
        return render_template("index.html")
    return redirect("/mywatchlist/result")


@app.post('/mywatchlist/search/user')
def search_user():
    data = {
        'username': request.form["username"]
    }
    user = User.get_by_username(data)
    return render_template('search_user.html', user=user)


@app.route('/mywatchlist/result/<int:id>')
def result_by_id(id):
    data = {
        'id': id,
        'myid': session['id']
    }
    followers = User.get_follower_user(data)
    followings = User.get_following_user(data)
    users = User.get_user_by_id(data)
    top5movie = Movie.get_top5movie(data)
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if Follow.get_following(data):
        followed = True
    else:
        followed = False
    return render_template("user.html", users=users, followers=followers, top5movie=top5movie, followed=followed, followings=followings)

@app.route('/mywatchlist/following/<int:id>')
def result_following_id(id):
    data = {
        'id': id
    }
    users = User.get_user_by_id(data)
    followings = User.get_following_user(data)
    return render_template("following_list.html", followings=followings, users=users)

@app.route('/mywatchlist/follower/<int:id>')
def result_follower_id(id):
    data = {
        'id': id,
        'myid': session['id']
    }
    users = User.get_user_by_id(data)
    followers = User.get_follower_user(data)
    followings = User.get_following_user(data)
    return render_template("follower_list.html", followers=followers, users=users, followings=followings)

@app.post('/mywatchlist/follow/<int:id>')
def to_follow_user(id):
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if not Follow.get_following(data):
        Follow.add_following(data)
        return redirect(f'/mywatchlist/result/{id}')
    return redirect(f'/mywatchlist/result/{id}')

@app.post('/mywatchlist/follow_fromlist/<int:id>')
def to_follow_user_fromlist(id):
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if not Follow.get_following(data):
        Follow.add_following(data)
        return redirect(f"/mywatchlist/follower/{session['id']}")
    return redirect(f"/mywatchlist/follower/{session['id']}")

@app.post('/mywatchlist/unfollow/<int:id>')
def to_unfollow_user(id):
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if Follow.get_following(data):
        Follow.delete_following(data)
        return redirect(f'/mywatchlist/result/{id}')
    return redirect(f'/mywatchlist/result/{id}')

@app.post('/mywatchlist/unfollow_fromlist/<int:id>')
def to_unfollow_user_fromlist(id):
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if Follow.get_following(data):
        Follow.delete_following(data)
        return redirect(f"/mywatchlist/follower/{session['id']}")
    return redirect(f"/mywatchlist/follower/{session['id']}")

@app.route('/mywatchlist/unfollow/<int:id>')
def to_unfollow_following_from_list(id):
    data = {
        'following_id': id,
        'follower_id': session['id']
    }
    if Follow.get_following(data):
        Follow.delete_following(data)
        return redirect(f"/mywatchlist/following/{session['id']}")
    return redirect(f"/mywatchlist/following/{session['id']}")


@app.post('/mywatchlist/register')
def register():
    if User.is_valid(request.form):

        user_in_db1 = User.get_by_email(request.form)
        user_in_db2 = User.get_by_username(request.form)

        if user_in_db1:
            flash("This email is used",'register')
            return redirect("/mywatchlist/")
        
        if user_in_db2:
            flash("This username is used",'register')
            return redirect("/mywatchlist/")

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "username" : request.form['username'],
            "email" : request.form['email'],
            "password" : pw_hash
        }
        id = User.register(data)
        session['id'] = id
        return redirect(f"/mywatchlist/result/{session['id']}")
    return redirect('/mywatchlist/')


@app.route("/mywatchlist/to_edit/<int:id>")
def to_edit_profile(id):
    if 'id' not in session:
        return redirect('/mywatchlist/')
    data = {
        'id': id
    }
    return render_template("edit_profile.html", user = User.get_user_by_id(data))


@app.post('/mywatchlist/edit/<int:id>')
def edit_profile(id):
    if 'id' not in session:
        return redirect('/mywatchlist/')
    data = {
        'id': id,
        "username" : request.form['username'],
        "movie_quote" : request.form['movie_quote'],
    }
    User.edit_profile(data)
    return redirect(f"/mywatchlist/result/{session['id']}")


@app.post('/mywatchlist/login')
def login():
    user_in_db = User.get_by_email(request.form)

    if not user_in_db:
        flash("Invalid Email/Password",'login')
        return redirect("/mywatchlist/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Username/Password",'login')
        return redirect('/mywatchlist/')
    session['id'] = user_in_db.id
    return redirect(f"/mywatchlist/result/{session['id']}")


@app.route('/mywatchlist/logout')
def logout():
    session.clear()
    return redirect('/mywatchlist/')
