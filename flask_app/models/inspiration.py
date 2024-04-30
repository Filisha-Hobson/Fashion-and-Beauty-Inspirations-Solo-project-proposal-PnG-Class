from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user

class Inspiration:
    db = 'mysolo_project'
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        
        self.inspire = None
        self.likes =[]
        
    @classmethod
    def save_this_post(cls,data):
        query = "INSERT INTO inspirations (description, user_id) VALUES(%(description)s, %(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def connect_viewer_to_post(cls):
        query = "SELECT * FROM inspirations LEFT JOIN users ON inspirations.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        
        createinspiration= [] #this is creating an empty list
        for row in results:
            grabinspo= cls(row)
            eachuser = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': None,
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            oneuser = user.User(eachuser)
            grabinspo.inspire = oneuser 
            #this is adding the objects to my empty list by appending
            createinspiration.append(grabinspo)
            likes_data = {
            'inspiration_id' : row['id']
            }

            grabinspo.likes = Inspiration.get_likes(likes_data)
            for like in grabinspo.likes:
                if like.id == session['user_id']:
                    grabinspo.logged_in_user_has_liked = True
        return createinspiration
    
    # #this method is selecting the id from the recipe
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM inspirations WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update_current_inspiration(cls,data):
        query = "UPDATE inspirations SET description = %(description)s WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    @classmethod
    def get_inspiration_by_id_with_viewer(cls,data):
        query = 'SELECT * FROM inspirations LEFT JOIN users ON inspirations.user_id = users.id WHERE inspirations.id = %(id)s;;'
        results = connectToMySQL(cls.db).query_db(query,data)
        if not results:
            return False
        getinspirationforviewer = results[0]
        inspiration= cls( getinspirationforviewer)
        eachuser = {
                'id':  getinspirationforviewer['users.id'],
                'first_name':  getinspirationforviewer['first_name'],
                'last_name':  getinspirationforviewer['last_name'],
                'email':  getinspirationforviewer['email'],
                'password': None,
                'created_at':  getinspirationforviewer['users.created_at'],
                'updated_at':  getinspirationforviewer['users.updated_at']
        }
        gettheuser = user.User(eachuser)
        inspiration.inspire = gettheuser
        return inspiration
    
    @classmethod
    def all_user_liked_inspirations(cls, data):
        query = 'SELECT inspiration_id as id FROM likes LEFT JOIN users on likes.user_id = users.id WHERE user_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        likes = []
        for row in results:
            likes.append(row['id'])
        return likes
    
    @classmethod
    def get_one_inspiration(cls, data):
        query = "SELECT * FROM inspirations LEFT JOIN likes ON inspirations.id = likes.inspiration_id LEFT JOIN users ON users.id = likes.user_id WHERE inspirations.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)

        inspiration = cls(results[0])

        for row in results:
            if row['users.id'] == None:
                break
            data = {
                'id':  row['users.id'],
                'first_name':  row['first_name'],
                'last_name':  row['last_name'],
                'email':  row['email'],
                'password': None,
                'created_at':  row['users.created_at'],
                'updated_at':  row['users.updated_at']
            }
            inspiration.likes.append(user.User(data))
        return inspiration
    
    @classmethod
    def get_likes(cls, data):
        query = "SELECT * FROM users LEFT JOIN likes ON likes.user_id = users.id WHERE likes.inspiration_id = %(inspiration_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        all_likes = []
        for row in results:
            all_likes.append(user.User(row))
        return all_likes

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (inspiration_id, user_id) VALUES ( %(inspiration_id)s, %(user_id)s );'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE inspiration_id = %(inspiration_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete_all_likes(cls, data):
        query = "DELETE FROM likes WHERE inspiration_id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def diminish(cls,data):
        query = 'DELETE FROM inspirations WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def val_inspiration(inspiration):
        is_valid = True
        if len(inspiration['description']) < 20:
            flash('Minimum of 20 characters.', 'inspo')
            is_valid = False
        return is_valid