from flask import render_template, request, redirect
from app_files import app, db
from app_files.models import Post, User, LoginForm, RegisterForm
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect('/home')
        else:
            error = 'Invalid credentials'

    return render_template('login.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists or email_exists:
            error = "There is already a user registered with that username or email in the system."
        elif form.password.data != form.passwordRetype.data:
            error = "The two passwords you have entered do not match."
        else:
            new_user = User(username=username, email=email, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            message = "You have successfully created an account. Please log in!"

            return render_template('login.html', form=LoginForm(), message=message)

    return render_template('register.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        user = User.query.get(current_user.id)

        new_post = Post(title=post_title, content=post_content, author=user.username)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/home')

    return render_template('create.html')


@app.route('/home')
@login_required
def home():
    all_posts = Post.query.order_by(desc(Post.date)).all()
    username = User.query.get(current_user.id).username
    return render_template('home.html', posts=all_posts, current_user=username)
