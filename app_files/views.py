from flask import render_template, request
from app_files import app, db
from app_files.models import Post, User
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length


@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    shouldRemember = BooleanField('remember me')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        login_user(user)

        # if user:
        #     current_user_id = user.id
        # else:
        #     user = User(username=username, email="default@gmail.com", password=password)
        #     db.session.add(user)
        #     db.session.commit()

        return render_template('home.html')
    else:
        return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are now logged out!'


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = current_user.id

        new_post = Post(title=post_title, content=post_content, user_id=post_author)
        db.session.add(new_post)
        db.session.commit()

    return render_template('create.html')


@app.route('/home')
@login_required
def home():
    all_posts = Post.query.order_by(desc(Post.date)).all()
    return render_template('home.html', posts=all_posts)
