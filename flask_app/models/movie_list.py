from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.movie import Movie


DB = "mywatchlist_schema"

class Movie_list:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.movies=[]

    @classmethod
    def add_movie_list(cls, data):
        query = "INSERT INTO movie_list (user_id, updated_at, created_at) VALUES (%(user_id)s, NOW(), NOW());"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_last_movie(cls):
        query = "SELECT * FROM movie_list ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL(DB).query_db(query)
        return cls(results[0])

    @classmethod
    def get_one_movie_in_user(cls, data):
        query = "SELECT * FROM movie_list JOIN movie_on_list ON movie_list_id = movie_list.id WHERE user_id = %(user_id)s AND movie_id = %(movie_id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def get_watchedmovies_by_user(cls, data):
        query = """
                SELECT * FROM users LEFT JOIN 
                (SELECT poster_path, user_id, director, title, watch_time, movie_on_list.id AS onlistid, movie_list_id, top5movie, movie_id, created_at, updated_at, 
                movie_list.id AS id FROM movie_list LEFT JOIN movie_on_list ON movie_list.id = movie_list_id WHERE watch_time != 0) to_watch_list 
                ON user_id = users.id WHERE users.id = %(id)s ORDER BY watch_time DESC;
                """
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        movie_list_data = { 
            **results[0],
            'id': results[0]['to_watch_list.id'],
            'created_at' : results[0]['to_watch_list.created_at'],
            'updated_at' : results[0]['to_watch_list.updated_at'],
        }
        user = cls( movie_list_data )
        for row_from_db in results:

            movie_data = {
                **row_from_db,
                "id" : row_from_db["onlistid"]
            }
            user.movies.append(Movie(movie_data))
        return user


    @classmethod
    def get_towatchmovies_by_user(cls, data):
        query = """
                SELECT * FROM users LEFT JOIN 
                (SELECT poster_path, user_id, director, title, watch_time, movie_on_list.id AS onlistid, movie_list_id, top5movie, movie_id, created_at, updated_at, 
                movie_list.id AS id FROM movie_list LEFT JOIN movie_on_list ON movie_list.id = movie_list_id WHERE watch_time = 0) to_watch_list 
                ON user_id = users.id WHERE users.id = %(id)s ORDER BY title ASC;
                """
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        movie_list_data = { 
            **results[0],
            'id': results[0]['to_watch_list.id'],
            'created_at' : results[0]['to_watch_list.created_at'],
            'updated_at' : results[0]['to_watch_list.updated_at'],
        }
        user = cls( movie_list_data )
        for row_from_db in results:

            movie_data = {
                **row_from_db,
                "id" : row_from_db["onlistid"]
            }
            user.movies.append(Movie(movie_data))
        return user

