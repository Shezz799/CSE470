from flask import request, redirect, url_for, Blueprint, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User, Customer, Admin
from models.database import db
from views.auth_views import AuthViews


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('dashboard.index'))
    
    return AuthViews.render_login()

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        business_name = request.form.get('business_name')
        

        if not phone or len(phone) < 10:
            flash('Please enter a valid phone number', 'error')
            return redirect(url_for('auth.signup'))
        
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', 'error')
            return redirect(url_for('auth.signup'))
        
        if user_type == 'business' and not business_name:
            flash('Business name is required', 'error')
            return redirect(url_for('auth.signup'))
        
        new_user = Customer(
            email=email,
            username=name,
            phone=phone,
            customer_type=user_type,
            business_name=business_name if user_type == 'business' else None
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Successfully registered! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return AuthViews.render_signup()

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
