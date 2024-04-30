from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = 'mysolo_project'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updates_at = data['updated_at']
        
    @classmethod
    def remember(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)
        
    @classmethod
    def get_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return None
    
    @staticmethod
    def val_email(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash('Email is already taken.', 'register')
            is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash('Email is Invalid!!!', 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters', 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if user['password'] != user['password_confirm']:
            flash("Password doesn't match", "register")
        return is_valid