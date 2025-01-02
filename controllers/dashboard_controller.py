from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models.database import db
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from constants import DISTRICTS

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@dashboard_bp.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    if request.method == 'POST':
        try:

            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            business_name = request.form.get('business_name')
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            

            pickup_area = request.form.get('pickup_area')
            pickup_house = request.form.get('pickup_house')
            pickup_street = request.form.get('pickup_street')
            pickup_address = request.form.get('pickup_address')

 
            user = User.query.get(current_user.id)
            user.username = username
            user.email = email
            user.phone = phone
            
            if business_name and current_user.type == 'customer' and current_user.customer_type == 'business':
                user.business_name = business_name


            user.pickup_area = pickup_area
            user.pickup_house = pickup_house
            user.pickup_street = pickup_street
            user.pickup_address = pickup_address


            if current_password and new_password:
                if not check_password_hash(user.password, current_password):
                    return jsonify({'error': 'Current password is incorrect'}), 400
                user.password = generate_password_hash(new_password)

            db.session.commit()
            return jsonify({'success': True})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500



    return render_template('account_settings.html', districts=DISTRICTS)
