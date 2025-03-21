import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from src.api_v1.users import api


auth_bp = Blueprint(
    'auth',
    __name__,
    url_prefix="/auth",
)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user')
    if user_id is None:
        g.user = None
    else:
        g.user = api.get_user_by_id(user_id)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = api.get_user_by_username(username)
        if user and user.check_password(password):
            session['user'] = user.id
            return redirect(url_for('blog.index'))
        else:
            error = 'Неправильное имя пользователя или пароль'
        flash(error)
    return render_template('login.html')
