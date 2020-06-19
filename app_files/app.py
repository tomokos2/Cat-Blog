from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Create the flask app
app = Flask(__name__)

app.config.from_pyfile('config.py')

# Load views after the app is instantiated
from app_files.views import *

# Set up the database
db = SQLAlchemy(app)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Set up bootstrap
Bootstrap(app)


if __name__ == '__main__':
    app.run()
