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
    def get_following_user(cls,data):
        query = """SELECT users.username AS follower, users2.username AS following, follows.* 
            FROM users LEFT JOIN follows ON users.id = follows.following_id 
            LEFT JOIN users AS users2 ON users2.id = follows.follower_id WHERE users2.id = %(id)s;
        """
        results = connectToMySQL(DB).query_db(query,data)
        followings = []
        for result in results:
            followings.append(cls(result))
        return followings

    @classmethod
    def add_following_list(cls, data):
        query = "INSERT INTO follows (follower_id, following_id, updated_at, created_at) VALUES (%(user_id)s,  , NOW(), NOW());"
        results = connectToMySQL(DB).query_db(query, data)
        return results

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

