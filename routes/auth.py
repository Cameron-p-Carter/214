from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Logic for logout
    return redirect(url_for('main.index'))
