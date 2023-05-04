import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db
from .seeds import seed_commands
from flask_cors import CORS
from .config import Config



# instantiate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instantiate the db
db.init_app(app)


# instantiate the migrate
Migrate(app, db)


# Tell flask about our seed commands
app.cli.add_command(seed_commands)
# Application Security
CORS(app)

