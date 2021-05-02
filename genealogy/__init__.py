import os
from sqlalchemy import MetaData
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session.__init__ import Session
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed

app = Flask(__name__, static_url_path='/genealogy/static/photos')

app.config["SECRET_KEY"] = "mysecretkey"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

app.config['SESSION_SQLALCHEMY'] = db

sess = Session(app)

Migrate(app, db, render_as_batch=True)

Moment(app)

Bootstrap(app)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'photos'

configure_uploads(app, photos)

from genealogy.individual.views import genealogy_blueprint

app.register_blueprint(genealogy_blueprint,url_prefix="/individual")
