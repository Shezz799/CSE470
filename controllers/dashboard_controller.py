from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.database import db
from models.user import User

dashboard_bp = Blueprint('dashboard', __name__)

DISTRICTS = [
    "Dhaka", "Faridpur", "Gazipur", "Gopalganj", "Jamalpur", "Kishoreganj",
    "Madaripur", "Manikganj", "Munshiganj", "Mymensingh", "Narayanganj",
    "Narsingdi", "Netrokona", "Rajbari", "Shariatpur", "Sherpur", "Tangail",
    "Bogra", "Joypurhat", "Naogaon", "Natore", "Nawabganj", "Pabna",
    "Rajshahi", "Sirajgonj", "Dinajpur", "Gaibandha", "Kurigram",
    "Lalmonirhat", "Nilphamari", "Panchagarh", "Rangpur", "Thakurgaon",
    "Barguna", "Barisal", "Bhola", "Jhalokati", "Patuakhali", "Pirojpur",
    "Bandarban", "Brahmanbaria", "Chandpur", "Chittagong", "Comilla",
    "Cox's Bazar", "Feni", "Khagrachari", "Lakshmipur", "Noakhali",
    "Rangamati", "Habiganj", "Maulvibazar", "Sunamganj", "Sylhet",
    "Bagerhat", "Chuadanga", "Jessore", "Jhenaidah", "Khulna", "Kushtia",
    "Magura", "Meherpur", "Narail", "Satkhira"
]

@dashboard_bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard.html')

@dashboard_bp.route('/add-parcel')
@login_required
def add_parcel():
    return render_template('add_parcel.html', districts=DISTRICTS)

@dashboard_bp.route('/account-settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        business_name = request.form.get('business_name')

        if not phone or len(phone) != 11:
            flash('Please enter a valid phone number', 'error')
            return redirect(url_for('dashboard.account_settings'))

        current_user.username = username
        current_user.email = email
        current_user.phone = phone

        if hasattr(current_user, 'customer_type') and current_user.customer_type == 'business':
            current_user.business_name = business_name

        if current_password and new_password:
            if not check_password_hash(current_user.password_hash, current_password):
                flash('Current password is incorrect', 'error')
                return redirect(url_for('dashboard.account_settings'))
            current_user.set_password(new_password)

        db.session.commit()
        flash('Account settings updated successfully', 'success')
        return redirect(url_for('dashboard.account_settings'))

    return render_template('account_settings.html')
