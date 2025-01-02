from flask import render_template, redirect, url_for
from flask_login import current_user

class AuthViews:
    @staticmethod
    def render_login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('auth/login.html')
    

    @staticmethod
    def render_signup(districts=None):
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('auth/signup.html', districts=districts)
