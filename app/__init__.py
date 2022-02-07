import imp
from operator import imod
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_ckeditor import CKEditor

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)
ckeditor = CKEditor(app)


app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'  # this value can be endpoint or url

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = 'You must be logged in to access this page'
login_manager.login_view = 'auth.login'

from app import routes
from .admin import admin as admin_blueprint
from .auth import auth as auth_blueprint
from .home import home as home_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(auth_blueprint)
app.register_blueprint(home_blueprint)