from flask import Flask
from config import Config
from flask_login import LoginManager #for logging users in and maintaining a session
from flask_sqlalchemy import SQLAlchemy #this talk to our database for us
from flask_migrate import Migrate #Makes altering the Database a lot easier

app = Flask(__name__)
app.config.from_object(Config)
# init Login Manager
login = LoginManager(app)
#where to be sent if you are not logged in
login.login_view = 'login'
# init the database from_object
db = SQLAlchemy(app)
# init Migrate
migrate = Migrate(app,db)


from app import routes