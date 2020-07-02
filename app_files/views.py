import os

from flask import render_template, request, redirect
from app_files import app, db
from app_files.models import Post, User, Comment, LoginForm, RegisterForm, PostForm, CommentForm, EditForm
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename


# This is the home page
@app.route('/')
def index():
    # Finds a file called index.html inside the templates directory
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    # Will be triggered when the user posts the login form
    if form.validate_on_submit():

        # Get the information from the form
        username = form.username.data
        password = form.password.data

        # Find the user in the database
        user = User.query.filter_by(username=username).first()

        # The user entered valid credentials
        if user and user.password == password:
            login_user(user)
            return redirect('/home')
        else:
            # Either the user does not have an account, or their password was incorrect
            error = 'Invalid credentials'

    # Get request or invalid credentials
    # In the latter case, load the error on the page
    return render_template('login.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm()

    # The user posted the registration form
    if form.validate_on_submit():
        # Get the information from the form
        username = form.username.data
        email = form.email.data

        # See if the user's information is already in the database
        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email).first()

        if username_exists or email_exists:
            error = "There is already a user registered with that username or email in the system."
        elif form.password.data != form.passwordRetype.data:
            error = "The two passwords you have entered do not match."
        else:
            # The user entered valid and unique information, so add them to the database
            new_user = User(username=username, email=email, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()

            # Once they create their account, report success message and take them to the login page
            message = "You have successfully created an account. Please log in!"
            return render_template('login.html', form=LoginForm(), message=message)

    # Get request or invalid form entry
    # In the latter case, load the error onto the page
    return render_template('register.html', form=form, error=error)


@app.route('/logout')
@login_required
def logout():
    # Use flask login to log out.
    logout_user()
    # Take them back to the index page
    return render_template('index.html')


@app.route('/home/create', methods=['GET', 'POST'])
@login_required
def create():
    # This computer's path in order to save photos
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    form = PostForm()

    if request.method == 'POST':
        # The user submitted a post creation form
        if form.validate_on_submit():
            # Get the date from the form
            post_title = form.title.data
            post_content = form.content.data
            user = User.query.get(current_user.id)
            photo = form.image.data

            # Create the path for the image to be saved
            image_path = None
            # The photo is optional
            if photo:
                filename = secure_filename(photo.filename)
                filepath = os.path.join(ROOT_DIR, 'static', 'uploads', 'photos', filename)
                photo.save(filepath)
                image_path = "/uploads/photos/" + filename

            # Add the post to the database
            new_post = Post(title=post_title, content=post_content, author=user.username, image_path=image_path)
            db.session.add(new_post)
            db.session.commit()

        # Take them back to the homepage
        return redirect('/home')

    return render_template('create.html', form=form)


@app.route('/home/self')
@login_required
def user_home():
    # Consists of only the user's posts
    posts = User.query.get(current_user.id).posts
    return render_template('user_posts.html', posts=posts)


@app.route('/home/self/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    # Get the post to edit from the database
    post = Post.query.get_or_404(id)
    posts = User.query.get(current_user.id).posts
    form = EditForm()

    # Make sure that only the current user can edit their post
    if post.author != User.query.get(current_user.id).username:
        return render_template('403.html'), 403
    if request.method == 'POST':
        # The user submitted their edit
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()

            # Take them back to their page
            return redirect("/home/self")

    # Pre-load the data that was already written
    form.content.data = post.content
    form.title.data = post.title
    return render_template('user_posts.html', post_id=post.id, form=form, editing=True, posts=posts)


@app.route('/home/self/delete/<int:id>')
@login_required
def delete(id):
    # Get the post to delete from the database
    post = Post.query.get_or_404(id)

    # Make sure that only the current user can delete their post
    if post.author != User.query.get(current_user.id).username:
        return render_template('403.html'), 403

    # Remove from the database and go back to user home
    db.session.delete(post)
    db.session.commit()
    return redirect('/home/self')


@app.route('/home/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    # Make sure the post they wish to comment on is in the database
    post = Post.query.get_or_404(id)
    form = CommentForm()
    username = User.query.get(current_user.id).username

    if request.method == 'POST':
        # The user submitted a valid comment
        if form.validate_on_submit():

            # Add the comment to the database
            content = form.content.data
            new_comment = Comment(content=content, author=username, post_id=id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect('/home')

    # Make the comment page a clone of the home page but with a comment form
    all_posts = Post.query.order_by(desc(Post.date)).all()
    return render_template("comment.html", posts=all_posts, current_user=username, comment_post=id, form=form)


@app.route('/home')
@login_required
def home():
    # Make sure to have most recent posts at the top
    all_posts = Post.query.order_by(desc(Post.date)).all()
    username = User.query.get(current_user.id).username
    return render_template('home.html', posts=all_posts, current_user=username)
