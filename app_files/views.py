from flask import render_template
from app_files.app import app
from app_files.models import Post
from sqlalchemy import desc


@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


@app.route('/home')
def home():
    all_posts = Post.query.order_by(desc(Post.date_posted)).all()
    return render_template('home.html', posts=all_posts)
