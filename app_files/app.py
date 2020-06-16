from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the flask app
app = Flask(__name__)

app.config.from_pyfile('config.py')

# Load views after the app is instantiated
from app_files.views import *

# Set up the database
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
