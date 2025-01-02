from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from models.parcel import Parcel
from models.database import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'admin':
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/manage-parcels')
@login_required
@admin_required
def manage_parcels():

    parcels = Parcel.query.order_by(Parcel.created_at.desc()).all()
    

    delivered_count = sum(1 for p in parcels if p.status == 'delivered')
    pending_count = sum(1 for p in parcels if p.status in ['pending', 'in_transit'])
    
    return render_template('manage_parcels.html',
                         parcels=parcels,
                         delivered_count=delivered_count,
                         pending_count=pending_count)

@admin_bp.route('/update-parcel-status/<int:parcel_id>', methods=['POST'])
@login_required
@admin_required
def update_parcel_status(parcel_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
            
        parcel = Parcel.query.get_or_404(parcel_id)
        parcel.status = new_status
        db.session.commit()
        

        all_parcels = Parcel.query.all()
        delivered_count = sum(1 for p in all_parcels if p.status == 'delivered')
        pending_count = sum(1 for p in all_parcels if p.status in ['pending', 'in_transit'])
        
        return jsonify({
            'success': True,
            'delivered_count': delivered_count,
            'pending_count': pending_count
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/parcel-details/<int:parcel_id>')
@login_required
@admin_required
def parcel_details(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    
    return jsonify({
        'id': parcel.id,
        'user': {
            'username': parcel.user.username,
            'email': parcel.user.email,
            'phone': parcel.user.phone
        },
        'invoice_number': parcel.invoice_number,
        'pickup_name': parcel.pickup_name,
        'pickup_area': parcel.pickup_area,
        'pickup_house': parcel.pickup_house,
        'pickup_street': parcel.pickup_street,
        'pickup_address': parcel.pickup_address,
        'pickup_contact': parcel.pickup_contact,
        'dropoff_name': parcel.dropoff_name,
        'dropoff_area': parcel.dropoff_area,
        'dropoff_house': parcel.dropoff_house,
        'dropoff_street': parcel.dropoff_street,
        'dropoff_address': parcel.dropoff_address,
        'dropoff_contact': parcel.dropoff_contact,
        'weight': parcel.weight,
        'fragile': parcel.fragile,
        'amount': parcel.amount,
        'instructions': parcel.instructions,
        'status': parcel.status,
        'created_at': parcel.created_at.isoformat()
    })



@admin_bp.route('/manage-payments')
@login_required
@admin_required
def manage_payments():


    parcels = Parcel.query.order_by(Parcel.created_at.desc()).all()
    

    total_received = sum(p.amount for p in parcels if p.payment_status == 'paid')
    total_pending = sum(p.amount for p in parcels if p.payment_status == 'pending')
    
    return render_template('manage_payments.html',
                         parcels=parcels,
                         total_received=total_received,
                         total_pending=total_pending)

@admin_bp.route('/update-payment-status/<int:parcel_id>', methods=['POST'])
@login_required
@admin_required
def update_payment_status(parcel_id):
    try:
        
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
            
        parcel = Parcel.query.get_or_404(parcel_id)
        parcel.payment_status = new_status
        parcel.payment_updated_at = datetime.utcnow()
        db.session.commit()
        

        all_parcels = Parcel.query.all()
        total_received = sum(p.amount for p in all_parcels if p.payment_status == 'paid')
        total_pending = sum(p.amount for p in all_parcels if p.payment_status == 'pending')
        
        return jsonify({
            'success': True,
            'total_received': total_received,
            'total_pending': total_pending
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payment-details/<int:parcel_id>')
@login_required
@admin_required
def payment_details(parcel_id):
    parcel = Parcel.query.get_or_404(parcel_id)
    
    return jsonify({
        'id': parcel.id,
        'user': {
            'username': parcel.user.username,
            'email': parcel.user.email,
            'phone': parcel.user.phone
        },
        'invoice_number': parcel.invoice_number,
        'amount': parcel.amount,
        'payment_status': parcel.payment_status,
        'created_at': parcel.created_at.isoformat(),
        'payment_updated_at': parcel.payment_updated_at.isoformat() if parcel.payment_updated_at else None
    })
