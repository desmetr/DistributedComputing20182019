from flask import Flask
# from config import Config
from login.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


loginApp = Flask(__name__)
loginApp.config.from_object(Config)

loginDB = SQLAlchemy(loginApp)
migrate = Migrate(loginApp, loginDB)

login = LoginManager(loginApp)
login.login_view = "login"

# import routes
from login import routes