from flask import Flask, render_template, url_for, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import BooleanField
import sys
from lib.forms import RegisterForm, LoginForm, AdminForm
from lib.models import User, db
import re
import sqlite3
from data_manager  import find_book, books_info, add_favorite , remove_from_favorite, get_favorite_books
import logging

app = Flask(__name__)
logging.basicConfig(filename='log.log', level=logging.INFO)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
db.init_app(app)
bcrypt = Bcrypt(app)
admin = Admin(app)
admin.add_view(ModelView(User, db.session))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET'])
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    search_query = request.args.get('search', '')
    if search_query != "":
        books = find_book(search_query)
    else:
        books = books_info()
    return render_template('home.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        logging.info('User %s logged in', user)
        if user:
            password_match = bcrypt.check_password_hash(user.password, form.password.data)
            if password_match:
                session['user_id'] = user.user_id # store the user ID in the session
                if user.is_admin:
                    logging.info('user is admin and %s logged in', user)
                    return redirect(url_for('admin_panel'))
                return redirect(url_for('dashboard'))
    logging.warning('Invalid login attempt')
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    user_id = User.query.filter_by(user_id=session['user_id']).first().get_id()
    if request.method == 'GET':
        if request.args.get('search', '') != "":
            books = find_book(request.args.get('search', ''))
        else:
            if request.args.get('favorites') == 'true':
                books = get_favorite_books(user_id=user_id)
                print("boooks", books)
            else:
                books=books_info()
        return render_template('dashboard.html', books=books )
    
    data = request.get_json() 
    book_id = data.get('book_id')        
    if book_id != None:
        if book_id.startswith("like"):
            book_id = re.sub("[^0-9]", "", book_id)
            add_favorite(book_id, user_id)
            logging.info('User with ID %s add this book in favorites list', book_id)
        else:
            book_id = re.sub("[^0-9]", "", book_id)
            remove_from_favorite(book_id, user_id)
            logging.info('User with ID %s remove this book from favorites list', book_id)

    books = books_info()       

    return render_template('dashboard.html', books=books )




@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    session.pop('user_id', None)
    logging.info('User logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user.is_admin:
        logging.info('User with ID %s try to access admin panel', user)
        return redirect(url_for('dashboard'))

    form = AdminForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_admin=form.is_admin.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('admin_panel'))

    users = User.query.all()
    return render_template('admin.html', form=form, users=users)



if __name__ == "__main__":
    app.run(debug=True)