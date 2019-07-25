from flask import request, redirect, render_template, session, flash
from app import app, db
from models import Blog, User
import hashlib
import random
import string
from hashutils import check_pw_hash

# users are required to login to view some pages, the allowed_routes defines the ones they can view before logging in
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            flash('User does not exist', 'general_error')
            return render_template('login.html')
        if not check_pw_hash(password, user.pw_hash):
            flash('User password incorrect', 'general_error')
            return render_template('login.html')
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        general_error = ''
        username_errors = ''
        password_errors = ''
        verify_error = ''

        # checks if username is in the database already
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            general_error = "Duplicate user"
            flash(general_error, 'general_error')

        #username checks for an empty string and whether the string is valid
        if empty_string(username) or not valid_string(username):
            username_error='Not a valid username'
            flash(username_error, 'username_error')
            render_template('signup.html')

        #password checks for an empty string and whether the string is valid
        if empty_string(password) or not valid_string(password):
            password_error='Not a valid password'
            flash(password_error, 'password_error')
            render_template('signup.html')

        #verify password checks for an empty string and whether the password input and the verify password match. If they are not equal, it will display an error to the user.
        if empty_string(verify) or not is_equal(password, verify):
            verify_error='Passwords don\'t match'
            flash(verify_error, 'verify_error')
            render_template('signup.html')

        if not general_error and not username_errors and not password_errors and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/')
def index():
    users = User.query.filter_by().all()
    return render_template('index.html', users=users)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if empty_string(title):
            title_error = "Please enter a title"
            flash(title_error, 'title_error')
            return render_template('newpost.html', body=body)
        
        if empty_string(body):
            body_error = "Please enter a message"
            flash(body_error, 'body_error')
            return render_template('newpost.html', title=title)
   
        if empty_string(title_error) and empty_string(body_error):
            current_user = User.query.filter_by(username=session['username']).first()
            new_post = Blog(title, body, current_user)
            db.session.add(new_post)
            db.session.commit()
            post = Blog.query.filter_by(id=new_post.id).first()
            return redirect(f'/blog?id={post.id}')

    return render_template('newpost.html', title_error=title_error, body_error=body_error)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        posts = Blog.query.filter_by().all()
    if request.method == 'GET':
        posts = Blog.query.filter_by().all()
        post_id = request.args.get('id')
        user_id = request.args.get('userId')
        if post_id != None:
            posts = Blog.query.filter_by(id=post_id).first()
        if user_id != None:
            posts = Blog.query.filter_by(owner_id=user_id).all()
    return render_template('blog.html', posts=posts)
    

#BELOW ARE THE FUNCTIONS THAT ARE USED FOR THE FORM VALIDATIONS
#Test if a return value is an empty string
def empty_string(value):
    if(len(value) == 0):
        return True

#Test whether two variables are equal to one another
def is_equal(variable1, variable2):
    if variable1 == variable2:
        return True

#Test whether the text inputs are valid, meaning they are less than 3 or more characters but 20 or less and do not contain spaces
def valid_string(value):
    if len(value) >= 3 and len(value) <= 20 and not " " in value:
            return True


if __name__ == '__main__':
    app.run()