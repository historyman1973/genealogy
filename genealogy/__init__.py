import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

Migrate(app, db)

from genealogy.individual.views import genealogy_blueprint

app.register_blueprint(genealogy_blueprint,url_prefix="/individual")
