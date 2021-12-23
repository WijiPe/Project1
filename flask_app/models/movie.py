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


    # @classmethod
    # def add_towatchlist(cls, data):
    #     query = "INSERT INTO to_watch_lists (title, user_id, updated_at, created_at) VALUES (%(title)s,%(user_id)s, NOW(), NOW())"
    #     results = connectToMySQL(DB).query_db(query, data)
    #     return results
    
    # @classmethod
    # def get_movies(cls):
    #     query = "SELECT * FROM moviess;"
    #     results = connectToMySQL(DB).query_db(query)
    #     print(results)
    #     movies= []
    #     for result in results:
    #         movies.append(cls(result))
    #     return movies

    
    # @classmethod
    # def get_one_top5movie(cls, data):
    #     query = "SELECT * FROM movies LEFT JOIN top5movies ON movies.id = movie_id LEFT JOIN users ON users.id = user_id WHERE movies.id = %(id)s;"
    #     results = connectToMySQL(DB).query_db(query, data)
    #     return cls(results[0])

    # @classmethod
    # def add_top5(cls, data):
    #     query = """
    #         INSERT INTO top5movies (movie_id, movie_id, created_at, updated_at) 
    #         VALUE (%(movie_id)s,%(movie_id)s, NOW(), NOW());
    #     """
    #     results = connectToMySQL(DB).query_db(query,data)
    #     return results


    # @classmethod
    # def edit_movie_by_user_id(cls, data):
    #     query = """
    #         UPDATE movies SET model = %(model)s, make=%(make)s, price=%(price)s, description=%(description)s, year=%(year)s, 
    #         created_at =NOW(), updated_at= NOW() WHERE id = %(id)s;
    #         """
    #     return connectToMySQL(DB).query_db(query,data)

    # @classmethod
    # def get_cars_show_owner(cls):
    #     query = "SELECT * FROM cars JOIN users ON users.id = cars.user_id;"
    #     results = connectToMySQL(DB).query_db(query)
    #     print(results)
    #     car = []
    #     for result in results:
    #         car.append(cls(result))
    #     return car

    # @classmethod
    # def add_car(cls,data):
    #     query = """
    #         INSERT INTO cars (model, make, year, price, description, created_at, updated_at, user_id) 
    #         VALUE (%(model)s,%(make)s, %(year)s, %(price)s, %(description)s, NOW(), NOW(), %(user_id)s);
    #     """
    #     results = connectToMySQL(DB).query_db(query,data)
    #     return results

    # @classmethod
    # def get_one_car(cls,data):
    #     query = "SELECT * FROM cars WHERE id = %(id)s;"
    #     results = connectToMySQL(DB).query_db(query,data)
    #     return cls(results[0])


    # @classmethod
    # def edit_car(cls,data):
    #     query = """
    #         UPDATE cars SET model = %(model)s, make=%(make)s, price=%(price)s, description=%(description)s, year=%(year)s, 
    #         created_at =NOW(), updated_at= NOW() WHERE id = %(id)s;
    #     """
    #     results = connectToMySQL(DB).query_db(query,data)
    #     return results


    
    # @classmethod
    # def get_one_car_show_owner(cls,data):
    #     query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
    #     results = connectToMySQL(DB).query_db(query,data)
    #     car = cls(results[0])
    #     return car

    # @classmethod
    # def get_car_from_owner(cls,data):
    #     query = "SELECT * FROM cars LEFT JOIN users ON users.id = cars.user_id WHERE users.id = %(id)s;"
    #     results = connectToMySQL(DB).query_db(query,data)
        
    #     car = cls(results[0])

    #     for row_from_db in results:
    #         seller_data = {
    #             "id" : row_from_db["users.id"],
    #             "first_name" : row_from_db["first_name"],
    #             "last_name" : row_from_db["last_name"],
    #             "email" : row_from_db["email"],
    #             "password" : row_from_db["password"],
    #             "created_at" : row_from_db["users.created_at"],
    #             "updated_at" : row_from_db["users.updated_at"]
    #         }
    #         car.users.append(User(seller_data))
    #     return car


    # @staticmethod
    # def is_valid(car):
    #     is_valid = True
    #     if len(car['model']) < 2:
    #         is_valid = False
    #         flash ('Model must be at least 3 characters.','name')
    #     if len(car['description']) < 3:
    #         is_valid = False
    #         flash ('Description must be at least 3 characters.','name')
    #     if len(car['make']) < 3:
    #         is_valid = False
    #         flash ('Make must be at least 3 charactors.','name')
    #     if 'year' not in car:
    #         is_valid = False
    #         flash ('Please select the year','name')
    #     if 'price' not in car:
    #         is_valid = False
    #         flash ('Please select the price','name')
    #     return is_valid

    # @classmethod
    # def purchase_car(cls,data):
    #     query = """
    #         UPDATE cars SET user_id = %(user_id)s, sold=1 WHERE id = %(id)s;
    #     """
    #     results = connectToMySQL(DB).query_db(query,data)
    #     return results

    # @classmethod 
    # def get_last(cls):
    #     query = "SELECT * FROM cars ORDER BY id DESC LIMIT 1;"
    #     results = connectToMySQL(DB).query_db(query)
    #     cars = []
    #     for car in results:
    #         cars.append( cls(car) )
    #     return cars