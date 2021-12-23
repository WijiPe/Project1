from flask import render_template, redirect, request, session
from werkzeug.wrappers import response
from flask_app.models.user import User
from flask_app.models.movie import Movie
from flask_app.models.movie_list import Movie_list
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
import requests
import json
bcrypt = Bcrypt(app)

def get_director(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=c49e028232019660cab8e28bf4d018d9&language=en-US')
    data = json.loads(response.text)
    for crew in data['crew']:
        if crew['job'] == 'Director':
            return crew['name']
    return "not found"

@app.route("/to_show/<int:id>")
def show_movies_list(id):
    data = {
        'id': id
    }
    count1 = Movie.count_towatch_movie(data)
    towatchmovies = Movie_list.get_towatchmovies_by_user(data)
    # count1 = len(towatchmovies.movies)
    count2 = Movie.count_watched_movie(data)
    watchedmovies = Movie_list.get_watchedmovies_by_user(data)
    # count2 = len(watchedmovies.movies)
    return render_template('movie_list.html', watchedmovies=watchedmovies, towatchmovies=towatchmovies, count1=count1, count2=count2)

@app.route("/to_show/movies/<int:page>")
def to_show_movies(page):
    response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key=c49e028232019660cab8e28bf4d018d9&language=en-US&page={page}')
    data = json.loads(response.text)
    print(data)
    data2={
        'id': session['id']
    }
    users= User.get_user_by_id(data2)
    return render_template('movies.html', data=data, users=users)

@app.route('/delete/movie_list/<int:id>')
def delete_movie_list(id):
    data = {
        'id': id,
        'user_id': session['id'],
    }
    Movie.delete_movie_list(data)
    return redirect(f"/to_show/{data['user_id']}")

@app.post("/add_top5movie")
def add_top5movie():
    data = {
        'movie_list_id': request.form['movie_list_id'],
        'id': session['id'],
    }
    if len(Movie.get_top5movie(data)) < 5:
        Movie.add_top5movie(data)
    return redirect(f'/to_show/{session["id"]}')


@app.route('/delete/top5movie/<int:id>')
def delete_top5movie(id):
    data = {
        'id': id,
    }
    Movie.delete_top5movie(data)
    return redirect("/result")

@app.route("/move_to_watchedlist/<int:id>")
def move_list(id):
    data = {
        'id': id,
        'user_id': session['id'],
    }
    Movie.move_to_watchedlist(data)
    return redirect(f'/to_show/{session["id"]}')

@app.route("/movie_detail/<int:id>")
def show_movie_detail(id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=c49e028232019660cab8e28bf4d018d9&language=en-US')
    data = json.loads(response.text)
    data2 = {
        'id': session['id']
    }
    users= User.get_user_by_id(data2)
    return render_template('movie_details.html', data=data, users=users)

@app.post('/search/movies')
def search_movies():
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key=c49e028232019660cab8e28bf4d018d9&language=en-US&query={request.form["movie"]}&page=1&include_adult=false')
    data = json.loads(response.text)
    data2 = {
        'id': session['id']
    }
    users= User.get_user_by_id(data2)
    return render_template('movies.html', data=data, users=users)


@app.post('/count_watchtime')         
def count_watchtime():
    data ={
        'id':request.form['movie_list_id']
    }
    Movie.add_watchtime(data)
    return redirect(f'/to_show/{session["id"]}')

@app.post("/add_watchedlist")
def add_watchedlist():
    data = {
        'user_id': session['id'],
        'title': request.form['movie_title'],
        'movie_id': request.form['movie_id'],
        'watch_time': 1,
        'director': get_director(request.form['movie_id']),
        'poster_path': request.form['poster_path']
    }
    if len(Movie_list.get_one_movie_in_user(data)) == 0:
        print(len(Movie_list.get_one_movie_in_user(data)))
        Movie_list.add_movie_list(data)
        movies = Movie_list.get_last_movie()
        data['movie_list_id']=movies.id
        Movie.add_movie_on_list(data)
        return redirect(f"/to_show/{data['user_id']}")
    return redirect (f"/to_show/movies/{request.form['page']}")



@app.post("/add_towatchlist")
def add_towatchlist():
    data = {
        'user_id': session['id'],
        'title': request.form['movie_title'],
        'movie_id': request.form['movie_id'],
        'watch_time': 0,
        'director': get_director(request.form['movie_id']),
        'poster_path': request.form['poster_path']
    }
    if len(Movie_list.get_one_movie_in_user(data)) == 0:
        print(len(Movie_list.get_one_movie_in_user(data)))
        Movie_list.add_movie_list(data)
        movies = Movie_list.get_last_movie()
        data['movie_list_id']=movies.id
        Movie.add_movie_on_list(data)
        return redirect(f"/to_show/{data['user_id']}")
    return redirect (f"/to_show/movies/{request.form['page']}")


    
# @app.route("/to_show/movie_list")
# def show_movies_list():
#     data = {
#         'id': session['id']
#     }
#     towatchmovies = Movie_list.get_towatchmovies_by_user(data)
#     watchedmovies = Movie_list.get_watchedmovies_by_user(data)
#     return render_template('movie_list.html', watchedmovies=watchedmovies, towatchmovies=towatchmovies)


    #     'id': session['id']
    # 
    # top5movies = Movie.get_top5movie(data)
    # if len(top5movies) < 5:
    #     data2 = {
    #         **request.form,
    #         'user_id': session['id']
    #     }
    #     Movie.add_top5movie(data2)
    # return redirect(f'/to_show/{session["id"]}')

# @app.route('/show_top_5_movie')
# def show_result():
#     if 'id' not in session:
#         return redirect('/')
#     data = {
#         'id': session['id']
#     }
#     users = User.get_by_id(data)
#     cars = Car.get_last()
#     return render_template("owner_car.html", users=users, cars=cars)

# @app.route("/to_edit_top5movie/<int:id>")
# def to_edit_top_movie(id):
#     if 'id' not in session:
#         return redirect('/')
#     data = {
#         'id': id
#     }
#     cars = Car.get_one_car(data)
#     if cars.user_id == session['id']:
#         return render_template("edit_car.html", cars=cars)
#     return redirect('/')




# @app.route("/to_add")
# def to_add_movie():
#     if 'id' not in session:
#         return redirect('/')
#     return render_template ("add_car.html")







# @app.post('/add')
# def add_top5():
#     if 'id' not in session:
#         return redirect('/')
#     if Car.is_valid(request.form):
#         data = {
#             'user_id': session['id'],
#             **request.form
#         }
#         Car.add_car(data)
#         return redirect("/result")
#     return redirect('/to_add')

# @app.post('/edit/<int:id>')
# def edit_car(id):
#     if 'id' not in session:
#         return redirect('/')
#     if Car.is_valid(request.form):
#         data = {
#             'id': id,
#             'model': request.form['model'],
#             'make': request.form['make'],
#             'price': request.form['price'],
#             'description': request.form['description'],
#             'year': request.form['year'],
#         }
#         Car.edit_car(data)
#         return redirect("/result")
#     return redirect(f'/to_edit/{id}')




# @app.route('/purchase/car/<int:id>')
# def purchase_car(id):
#     if 'id' not in session:
#         return redirect('/')
#     data = {
#         "id":id,
#         "user_id":session['id']
#     }
#     cars = Car.purchase_car(data)
#     # return redirect('/result')
#     return redirect('/show_result')



