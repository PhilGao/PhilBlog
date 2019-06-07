from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CsrfProtect()
login_manager = LoginManager()