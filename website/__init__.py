from os.path import join, dirname, realpath

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, SQLAlchemyAdapter



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:@localhost/phpmyadmin/db_structure.php?db=flask_blogger'
app.secret_key = "super secret key"
db = SQLAlchemy(app)
db.init_app(app)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'upload\\')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = 'login' #redirection view for login
login_manager.init_app(app)

from website.models import User
# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db, User)  # Register the User model
user_manager = UserManager(db_adapter, app)  # Initialize Flask-User
