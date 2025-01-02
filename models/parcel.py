from datetime import datetime
from models.database import db

class Parcel(db.Model):
    __tablename__ = 'parcels'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('parcels', lazy=True))
    


    pickup_area = db.Column(db.String(100), nullable=False)
    pickup_name = db.Column(db.String(100), nullable=False)
    pickup_house = db.Column(db.String(50), nullable=False)
    pickup_street = db.Column(db.String(50), nullable=False)
    pickup_address = db.Column(db.String(200), nullable=False)
    pickup_contact = db.Column(db.String(20), nullable=False)
    


    dropoff_area = db.Column(db.String(100), nullable=False)
    dropoff_name = db.Column(db.String(100), nullable=False)
    dropoff_house = db.Column(db.String(50), nullable=False)
    dropoff_street = db.Column(db.String(50), nullable=False)
    dropoff_address = db.Column(db.String(200), nullable=False)
    dropoff_contact = db.Column(db.String(20), nullable=False)
    


    invoice_number = db.Column(db.String(50), nullable=False, unique=True)
    weight = db.Column(db.Float, nullable=False)
    fragile = db.Column(db.Boolean, default=False)
    amount = db.Column(db.Float, nullable=False)
    instructions = db.Column(db.Text)
    


    status = db.Column(db.String(20), default='pending') 
    payment_status = db.Column(db.String(20), default='unpaid') 
    payment_method = db.Column(db.String(20), default='Cash on Delivery')  
    payment_updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def status_display(self):
        return self.status.title()
    
    @property
    def payment_status_display(self):
        return self.payment_status.title()
