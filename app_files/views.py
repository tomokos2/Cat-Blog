from flask import render_template
from app_files.app import app


@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


