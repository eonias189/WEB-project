import flask
import datetime as dt
from flask import Flask, request, url_for, render_template, redirect, jsonify, make_response, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import db_session
from data.users import User
from flask_forms import RegisterForm

db_session.global_init("db/country_guesser.db")
session = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Country_Guesser_Secret_Key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


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
    params = {'title': 'Главная страница', 'styles': [main_css]}
    # base.html принимает параметры title и styles(список url css файлов)
    return render_template('main_page.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    main_css = url_for('static', filename='css/main_css.css')
    params = {'title': 'Регистрация', 'styles': [main_css,
                                                 url_for('static', filename='css/form_css.css')], 'form': form}
    if form.validate_on_submit():
        print(form.login.data)
    return render_template('register.html', **params)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
