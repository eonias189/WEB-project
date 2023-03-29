import flask
import requests
import datetime as dt
import data.users_resource
import data.question_resource

from flask import Flask, request, url_for, render_template, redirect, jsonify, make_response, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_restful import Api
from werkzeug.security import generate_password_hash
from data import db_session
from data.users import User
from data.api_key_tools import create_key
from flask_forms import RegisterForm, LoginForm

db_session.global_init("db/country_guesser.db")
session = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Country_Guesser_Secret_Key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)

api = Api(app)
api.add_resource(data.users_resource.UserResource, '/api/users/<int:user_id>')
api.add_resource(data.users_resource.UserListResource, '/api/users')
api.add_resource(data.users_resource.LoginResource, '/api/login')
api.add_resource(data.question_resource.QuestionResource, '/api/question')

login_manager = LoginManager()
login_manager.init_app(app)

button_style = "font-size:16px;border:1pxsolidgray;padding:3px;background-color:Green;border-radius:10px;"


@app.errorhandler(400)
def bad_request(error):
    return redirect('/error/Bad Request')


@app.errorhandler(404)
def not_found(error):
    return redirect('/error/Not Found')


@app.errorhandler(401)
def access_denied(_):
    return redirect('/error/Access Denied')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/')
def index():
    main_css = url_for('static', filename='css/main_css.css')
    params = {'title': 'Главная страница', 'styles': [main_css], 'user': current_user}
    # base.html принимает параметры title, styles(список url css файлов) и user(функцию current_user)
    return render_template('main_page.html', **params)


@app.route('/error/<message>')
def error_page(message):
    main_css = url_for('static', filename='css/main_css.css')
    params = {'title': 'Ошибка', 'styles': [main_css], 'user': current_user, 'message': message}
    return render_template('error.html', **params)


@app.route('/user/<int:user_id>')
def user_profile(user_id):
    main_css = url_for('static', filename='css/main_css.css')
    url = f'http://127.0.0.1:5000/api/users/{user_id}'
    paramss = {'key': create_key('GET')}
    response = requests.get(url, params=paramss).json()
    if 'user' not in response:
        return redirect(f'/error/{response["message"]}')
    params = {'title': response['user']['login'],
              'styles': [main_css, url_for('static', filename='css/profile_css.css')], 'user': current_user,
              'response': response['user']}
    return render_template('profile.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    main_css = url_for('static', filename='css/main_css.css')
    params = {'title': 'Регистрация', 'styles': [main_css, url_for('static', filename='css/form_css.css')],
              'form': form, 'user': current_user}
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', **params, message='Пароли не совпадают')
        messages_ru = {'Login is already taken': 'Этот логин уже занят'}
        url = 'http://127.0.0.1:5000/api/users'
        json = {'login': form.login.data, 'hashed_password': generate_password_hash(form.password.data)}
        paramss = {'key': create_key('POST')}
        response = requests.post(url, json=json, params=paramss).json()
        if 'error' in response:
            return render_template('register.html', **params, message=messages_ru[response['error']])
        return redirect('/')
    return render_template('register.html', **params)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    main_css = url_for('static', filename='css/main_css.css')
    params = {'title': 'Войти', 'styles': [main_css, url_for('static', filename='css/form_css.css')], 'form': form,
              'user': current_user}
    if form.validate_on_submit():
        login, password, remember_me = form.login.data, form.password.data, form.remember_me.data
        url = 'http://127.0.0.1:5000/api/login'
        json = {'login': login, 'password': password}
        paramss = {'key': create_key('LOGIN')}
        messages_ru = {'Login or password is wrong': 'Неверный логин или пароль'}
        response = requests.get(url, json=json, params=paramss).json()
        if 'error' in response:
            return render_template('login.html', **params, message=messages_ru[response['error']])
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(response['id'])
        login_user(user, remember=remember_me)
        return redirect('/')
    return render_template('login.html', **params)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
