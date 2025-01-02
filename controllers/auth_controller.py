from flask import request, redirect, url_for, Blueprint, flash, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User, Customer, Admin
from models.database import db
from views.auth_views import AuthViews
from constants import DISTRICTS

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            flash('Invalid email or password', 'error')
            return redirect(url_for('auth.login'))
            
        if user.type == 'admin':
            flash('Please use the admin login page', 'error')
            return redirect(url_for('auth.admin_login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('dashboard.index'))
    
    return render_template('login.html')

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.type == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, type='admin').first()
        
        if not user or not user.check_password(password):
            flash('Invalid admin credentials', 'error')
            return redirect(url_for('auth.admin_login'))
        
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin_login.html')

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
        
        pickup_district = request.form.get('pickup_district')
        pickup_name = request.form.get('pickup_name')
        pickup_house = request.form.get('pickup_house')
        pickup_street = request.form.get('pickup_street')
        pickup_detailed_address = request.form.get('pickup_detailed_address')

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
            business_name=business_name if user_type == 'business' else None,
            pickup_district=pickup_district,
            pickup_name=pickup_name,
            pickup_house=pickup_house,
            pickup_street=pickup_street,
            pickup_detailed_address=pickup_detailed_address
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Successfully registered! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html', districts=DISTRICTS)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
