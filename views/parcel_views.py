from flask import render_template
from flask_login import current_user

class ParcelViews:
    @staticmethod
    def render_add_parcel(districts):
        default_pickup = {
            'district': current_user.pickup_district,
            'name': current_user.pickup_name,
            'house': current_user.pickup_house,
            'street': current_user.pickup_street,
            'address': current_user.pickup_detailed_address,
            'phone': current_user.phone
        }
        return render_template('add_parcel.html', districts=districts, default_pickup=default_pickup)
        
    @staticmethod
    def render_my_parcels(parcels, completed_deliveries, processing_deliveries, cancelled_deliveries):
        return render_template('my_parcels.html',
                             parcels=parcels,
                             completed_deliveries=completed_deliveries,
                             processing_deliveries=processing_deliveries,
                             cancelled_deliveries=cancelled_deliveries)

    @staticmethod
    def render_payment_updates(pending_payments, total_paid, total_unpaid):
        return render_template('payment_updates.html',
                             pending_payments=pending_payments,
                             total_paid=total_paid,
                             total_unpaid=total_unpaid)
