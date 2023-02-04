from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Unpentable wall"

bcrypt = Bcrypt(app)
DATABASE = "dojo_project1_db"