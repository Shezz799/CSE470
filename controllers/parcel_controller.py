from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from models.database import db
from models.parcel import Parcel
from views.parcel_views import ParcelViews
from constants import DISTRICTS
import time

parcel_bp = Blueprint('parcel', __name__)

@parcel_bp.route('/add_parcel', methods=['GET', 'POST'])
@login_required
def add_parcel():
    if request.method == 'GET':
        return ParcelViews.render_add_parcel(districts=DISTRICTS)
        
    elif request.method == 'POST':
        try:
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form


            weight = float(data.get('weight', 0))
            amount = float(data.get('amount', 0))
            invoice_number = data.get('invoice_number')
            

            if not invoice_number:
                return jsonify({'error': 'Invoice number is required'}), 400
            

            existing_parcel = Parcel.query.filter_by(invoice_number=invoice_number).first()
            if existing_parcel:
                return jsonify({'error': 'Invoice number already exists'}), 400
            

            fragile = data.get('fragile', 'off') == 'on'

 


            pickup_area = data.get('pickup_area', '')
            dropoff_area = data.get('dropoff_area', '')
            
            if not pickup_area or not dropoff_area:
                return jsonify({'error': 'Please select both pickup and dropoff districts'}), 400
            


            parcel = Parcel(
                customer_id=current_user.id,
                pickup_area=pickup_area,
                pickup_name=data.get('pickup_name'),
                pickup_house=data.get('pickup_house'),
                pickup_street=data.get('pickup_street'),
                pickup_address=data.get('pickup_address'),
                pickup_contact=data.get('pickup_contact'),
                
                dropoff_area=dropoff_area,
                dropoff_name=data.get('dropoff_name'),
                dropoff_house=data.get('dropoff_house'),
                dropoff_street=data.get('dropoff_street'),
                dropoff_address=data.get('dropoff_address'),
                dropoff_contact=data.get('dropoff_contact'),
                
                invoice_number=invoice_number,
                weight=data.get('weight', type=float),
                fragile=data.get('fragile', type=bool),
                amount=amount,
                instructions=data.get('instructions'),
                payment_method=data.get('payment_method', 'Cash on Delivery')
            )
            
            db.session.add(parcel)
            db.session.commit()
            
            if request.is_json:
                return jsonify({
                    'message': 'Parcel created successfully',
                    'amount': amount
                }), 201
            else:
                return jsonify({'success': True})
            
        except Exception as e:
            current_app.logger.error(f"Error creating parcel: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

@parcel_bp.route('/my_parcels')
@login_required
def my_parcels():

    parcels = Parcel.query.filter_by(customer_id=current_user.id)\
        .order_by(Parcel.created_at.desc()).all()
    

    completed_deliveries = sum(1 for p in parcels if p.status == 'delivered')
    processing_deliveries = sum(1 for p in parcels if p.status in ['pending', 'picked_up', 'in_transit'])
    cancelled_deliveries = sum(1 for p in parcels if p.status == 'cancelled')
    
    return ParcelViews.render_my_parcels(
        parcels=parcels,
        completed_deliveries=completed_deliveries,
        processing_deliveries=processing_deliveries,
        cancelled_deliveries=cancelled_deliveries
    )

@parcel_bp.route('/payment_updates')
@login_required
def payment_updates():



    parcels = Parcel.query.filter_by(customer_id=current_user.id).all()
    


    total_paid = sum(p.amount for p in parcels if p.payment_status == 'paid')
    total_unpaid = sum(p.amount for p in parcels if p.payment_status == 'unpaid')
    

    pending_payments = [p for p in parcels if p.payment_status == 'unpaid']
    
    return ParcelViews.render_payment_updates(
        pending_payments=pending_payments,
        total_paid=total_paid,
        total_unpaid=total_unpaid
    )
