from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# Create the flask app
app = Flask(__name__)

app.config.from_pyfile('config.py')

# Set up bootstrap
Bootstrap(app)

# Load views after the app is instantiated
from app_files.views import *


# Set up the database
db = SQLAlchemy(app)

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run()
