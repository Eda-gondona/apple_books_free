
from flask import request, session, jsonify
import db
import webutil
import account
from webutil import app, login_required, get_myself
import logging

log = logging.getLogger("api.account")
#вход пользователя 
@app.route('/api/login', methods=['POST'])
def login():
    #получаем входные данные от пользователя или {}
    input = request.json or {}
    email = input.get('email')
    password = input.get('password')
    #если нет пароля или email то просто предупреждаем
    if not email or not password:
        return webutil.warn_reply("Missing input")
    #делаем запрос на поиск пользователя по id если такого пользователя нет или пароль хешированый и реальный не совподают
    u = db.get_user_by_email(email)
    if not u or not account.check_password(u.password, password):
        return webutil.warn_reply("Invalid login credentials")
    else:
        account.build_session(u, is_permanent=input.get('remember', True))
        log.info("LOGIN OK agent={}".format(webutil.get_agent()))
        return jsonify(u.serialize()), 200
#регистрация 
@app.route('/api/signup', methods=['POST'])
def signup():
    #получаем от пользователя данные 
    input = request.json or {}
    email = input.get('email')
    password = input.get('password')
    fname = input.get('fname')
    lname = input.get('lname')
    company = input.get('company')
    #если пользователеь не ввел email или что то другое
    if not email or not password or not fname or not lname:
        return webutil.warn_reply("Invalid signup input")
    #запрос на получения пользователя по id 
    u = db.get_user_by_email(email)
    if u:#
        msg = "Signup email taken: {}".format(email)
        return webutil.warn_reply(msg)
    #проверяем пароль 
    err = account.check_password_validity(password)
    if err:
        return jsonify({"err":err}), 400
    #записываем введеные данные пользователя в db
    u = db.User()
    u.email = email
    u.company = company
    u.first_name = fname
    u.last_name = lname
    u.password = account.hash_password(password)
    u.tags = []
    u.role = 'editor'
    u.save(force_insert=True)
    #создаем сессия и сериализуем введеные данные
    account.new_signup_steps(u)
    account.build_session(u, is_permanent=input.get('remember', True))
    log.info("SIGNUP OK agent={}".format(webutil.get_agent()))
    return jsonify(u.serialize()), 201
#выход  просто очищаем сессию
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({}), 200
#данные обо мне
@app.route('/api/me')
@login_required
def me():
    me = get_myself()
    reply = {"me": me.serialize()}
    return jsonify(reply), 200

@app.route('/api/users')
@login_required(role='superuser')
def users():
    input = request.args or {}
    page = input.get('page')
    size = input.get('size')
    search = input.get('search')

    reply = db.query_users(page, size, search)
    return jsonify([user.serialize() for user in reply]), 200 