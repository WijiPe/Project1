from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DB = "mywatchlist_schema"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.%]+@[a-zA-Z0-9.!&]+\.[a-zA-Z]+$')
PASSWORD_REGEX1 = re.compile (r'^.*[A-Z].*[0-9].*|.*[0-9].*[A-Z].*')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if 'followed' in data:
            self.followed = data['followed']
        if 'movie_quote' in data:
            self.movie_quote = data['movie_quote']

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (username, email, password, updated_at, created_at) VALUES (%(username)s, %(email)s, %(password)s, NOW(), NOW());"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            one_user = cls(results[0])
            print('this is the dictionary', results[0])
            print('this is the object', one_user)
            return one_user

    @classmethod
    def edit_profile(cls,data):
        query = """
            UPDATE users SET username = %(username)s, movie_quote=%(movie_quote)s, 
            created_at =NOW(), updated_at= NOW() WHERE id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query,data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            one_user = cls(results[0])
            print('this is the dictionary', results[0])
            print('this is the object', one_user)
            return one_user
    
    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            one_user = cls(results[0])
            print('this is the dictionary', results[0])
            print('this is the object', one_user)
            return one_user

    @classmethod
    def get_follower_user(cls,data):
        query = "SELECT *, follower_id in (SELECT following_id FROM follows WHERE follower_id = %(myid)s) AS followed FROM users JOIN follows ON users.id = follower_id WHERE following_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        followers = []
        for result in results:
            followers.append(cls(result))
        return followers

    @classmethod
    def get_following_user(cls,data):
        query = "SELECT * FROM users JOIN follows ON users.id = following_id WHERE follower_id = %(id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        followings = []
        for result in results:
            followings.append(cls(result))
        return followings
    
    @classmethod
    def get_following_user_who_list_movie_towatch(cls,data):
        query = """
            SELECT * FROM users JOIN movie_list ON users.id = user_id JOIN movie_on_list ON movie_list.id = movie_list_id 
            JOIN follows ON users.id = following_id WHERE follower_id = %(id)s and watch_time = 0 and movie_id = %(movie_id)s; 
        """
        results = connectToMySQL(DB).query_db(query,data)
        followers = []
        for result in results:
            followers.append(cls(result))
        return followers

    @classmethod
    def get_following_user_who_list_movie_watched(cls,data):
        query = """
            SELECT * FROM users JOIN movie_list ON users.id = user_id JOIN movie_on_list ON movie_list.id = movie_list_id 
            JOIN follows ON users.id = following_id WHERE follower_id = %(id)s and watch_time > 0 and movie_id = %(movie_id)s; 
        """
        results = connectToMySQL(DB).query_db(query,data)
        followers = []
        for result in results:
            followers.append(cls(result))
        return followers

    @classmethod
    def get_user_who_list_movie_towatch(cls,data):
        query = """
            SELECT * FROM users JOIN movie_list ON users.id = user_id JOIN movie_on_list ON movie_list.id = movie_list_id WHERE watch_time = 0 and movie_id = %(movie_id)s; 
        """
        results = connectToMySQL(DB).query_db(query,data)
        followers = []
        for result in results:
            followers.append(cls(result))
        return followers

    @classmethod
    def get_user_who_list_movie_watched(cls,data):
        query = """
            SELECT * FROM users JOIN movie_list ON users.id = user_id JOIN movie_on_list ON movie_list.id = movie_list_id WHERE watch_time > 0 and movie_id = %(movie_id)s; 
        """
        results = connectToMySQL(DB).query_db(query,data)
        followers = []
        for result in results:
            followers.append(cls(result))
        return followers

    @staticmethod
    def is_valid(user):
        is_valid = True
        if len(user['username']) < 3:
            is_valid = False
            flash ('Username must be at least 3 characters.','register')
        if not EMAIL_REGEX.match(user['email']):
            flash ("Invalid email address!")
        if len(user['password']) < 8:
            is_valid = False
            flash ('Password must be at least 8 charactors.','register')
        elif not PASSWORD_REGEX1.match(user['password']):
            is_valid = False
            flash ('Password must include uppercase letter.','register')
        return is_valid   

