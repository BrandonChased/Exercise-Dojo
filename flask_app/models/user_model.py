from flask import flash
from flask_app.config.mysqlconnections import connectToMySQL
from flask_app import DATABASE
from flask_app import bcrypt
import re

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.confirm_password = data["confirm_password"]
        self.updated_at = data["updated_at"]
        self.created_at = data["created_at"]
    

#**********************CREATE METHODS*********************
    @classmethod
    def created_user(cls,data):
        query = """
            INSERT INTO users(first_name,last_name,email,password)
            VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        """

        return connectToMySQL(DATABASE).query_db(query,data)

#**********************READMETHODS************************


#***********GET USER BY ID*****************

    @classmethod
    def get_user(cls,data): 
        query = """
            SELECT * FROM users
            WHERE id = %(id)s
        """
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])
        


#***********GET USER BY EMAIL*****************
    @classmethod
    def get_user_email(cls,data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s;
        """
        
        results = connectToMySQL(DATABASE).query_db(query,data)

        if results:
            return cls(results[0])


#**********************UPDATED METHODS********************

#**********************DELETE METHODS*********************


#**********************VALIDATIONS************************
    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data["first_name"]) < 3:
            flash("First name must be at least 3 characters","first_name")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("last name must be at least 3 characters","last_name")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Please enter a valid email address","email")
            is_valid = False
        if not PASSWORD_REGEX.match(data["password"]):
            flash("Password must have 1 uppcase letter,1 lowercase letter, and a number","password")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Passwords,do not match", "password")
            is_valid = False

        return is_valid
    
    @classmethod
    def validate_login(cls,data):

        found_user = cls.get_user_email(data)

        if not found_user:
            flash("Invalid login....",'login')
            return False
        elif not bcrypt.check_password_hash(found_user.password, data['password']):
            flash("Invalid login...",'login')
            return False
        
        return found_user