from flask import render_template, request
from app_files.app import app, db
from app_files.models import Post, User
from sqlalchemy import desc


current_user_id = None

@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user_id

    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            current_user_id = user.id
        else:
            user = User(username=username, email="default@gmail.com", password=password)
            db.session.add(user)
            db.commit()
    else:
        return render_template('login.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST' and current_user_id:
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = current_user_id

        new_post = Post(title=post_title, content=post_content, user_id=post_author)
        db.session.add(new_post)
        db.commit()

    return render_template('create.html')


@app.route('/home')
def home():
    all_posts = Post.query.order_by(desc(Post.date_posted)).all()
    return render_template('home.html', posts=all_posts)
