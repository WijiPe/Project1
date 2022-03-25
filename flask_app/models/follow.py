from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

DB = "mywatchlist_schema"

class Follow:
    def __init__( self , data ):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.follower_id = data['follower_id']
        self.following_id = data['following_id']

    @classmethod
    def add_following(cls, data):
        query = "INSERT INTO follows (following_id, follower_id, updated_at, created_at) VALUES (%(following_id)s, %(follower_id)s, NOW(), NOW());"
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_follower(cls, data):
        query = "SELECT * FROM follows WHERE following_id = %(following_id)s and follower_id = %(follower_id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            one_user = cls(results[0])
            print('this is the dictionary', results[0])
            print('this is the object', one_user)
            return one_user

    @classmethod
    def get_following(cls, data):
        query = "SELECT * FROM follows WHERE following_id = %(following_id)s and follower_id = %(follower_id)s;"
        results = connectToMySQL(DB).query_db(query,data)
        if results:
            one_user = cls(results[0])
            print('this is the dictionary', results[0])
            print('this is the object', one_user)
            return one_user
    
    @classmethod
    def delete_following(cls, data):
        query = "DELETE FROM follows WHERE following_id = %(following_id)s and follower_id = %(follower_id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return results