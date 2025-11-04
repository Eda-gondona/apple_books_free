import sys
import re
from flask import request, session
from passlib.context import CryptContext
import logging

log = logging.getLogger("account")

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"]
)
#создание сессии проверяем объект пользователя assert user_obj его id если нет то NOne 
def build_session(user_obj, is_permanent=True):
    assert user_obj
    assert user_obj.id
    #добавляем в данные сессии id и роль пользователя 
    session.clear()
    session['userid'] = user_obj.id
    session['role'] = user_obj.role
    session.permanent = is_permanent
#хеширование пароля
def hash_password(password):
    return pwd_context.hash(password)
#проверка хешированого пароля с реальным(еоторый вписал пользователь)
def check_password(hash, password):
    return pwd_context.verify(password, hash)
#проверка н асложность пароля 
def check_password_validity(passwd):
    err = None

    if not passwd or len(passwd) < 6:
        err = "Password must be atleast 6 characters"
    elif not re.search(r"[a-z]", passwd) \
            or not re.search(r"[A-Z]", passwd) \
            or not re.search(r"[0-9]", passwd):
        err = "Password must contain a lowercase, an uppercase, a digit"

    if err:
        log.error("password validity: %s", err)

    return err
#функция заглушка 
def new_signup_steps(user_obj):
    log.info("HELLO")
    pass