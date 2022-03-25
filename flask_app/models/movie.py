from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User


DB = "mywatchlist_schema"

class Movie:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.director = data['director']
        self.movie_id = data['movie_id']
        self.watch_time = data['watch_time']
        self.movie_list_id = data['movie_list_id']
        self.top5movie = data['top5movie']
        self.poster_path = data['poster_path']
    
    @classmethod
    def get_movies_by_user_id(cls, data):
        query = "SELECT * FROM movie_on_list LEFT JOIN movie_list ON movie_list.id = movie_list_id LEFT JOIN users ON users.id = user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        movies = []
        for result in results:
            movies.append(cls(result))
        return movies

    @classmethod
    def delete_movie_list(cls, data):
        query = "DELETE FROM movie_on_list WHERE movie_list_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def add_top5movie(cls, data):
        query = "UPDATE movie_on_list SET top5movie = 1 WHERE movie_list_id = %(movie_list_id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_top5movie(cls, data):
        query = "SELECT * FROM movie_on_list LEFT JOIN movie_list ON movie_list.id = movie_list_id WHERE user_id = %(id)s AND top5movie = 1;"
        results = connectToMySQL(DB).query_db(query, data)
        movies = []
        for result in results:
            movies.append(cls(result))
        return movies

    @classmethod
    def delete_top5movie(cls,data):
        query = "UPDATE movie_on_list SET top5movie = 0 WHERE movie_list_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def add_movie_on_list(cls, data):
        query = """
                INSERT INTO movie_on_list (title, director, movie_id, watch_time, movie_list_id, top5movie, poster_path) 
                VALUES (%(title)s,%(director)s, %(movie_id)s,%(watch_time)s, %(movie_list_id)s, 0, %(poster_path)s)
            """
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def move_to_watchedlist(cls, data):
        query = "UPDATE movie_on_list SET watch_time = 1 WHERE movie_list_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def add_watchtime(cls, data):
        query = "UPDATE movie_on_list SET watch_time = watch_time+1 WHERE movie_list_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def count_towatch_movie(cls, data):
        query = "SELECT COUNT(*) AS times FROM movie_list JOIN movie_on_list ON movie_list.id = movie_list_id WHERE user_id = 1 AND watch_time = 0;"
        results = connectToMySQL(DB).query_db(query,data)
        return results[0]['times']

    @classmethod
    def count_watched_movie(cls, data):
        query = "SELECT COUNT(*) AS times FROM movie_list JOIN movie_on_list ON movie_list.id = movie_list_id WHERE user_id = 1 AND watch_time != 0;"
        results = connectToMySQL(DB).query_db(query,data)
        return results[0]['times']

