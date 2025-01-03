from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(User):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    customer_type = db.Column(db.String(20), nullable=False)
    business_name = db.Column(db.String(100))
    
    pickup_district = db.Column(db.String(100), nullable=False)
    pickup_name = db.Column(db.String(100), nullable=False)
    pickup_house = db.Column(db.String(50), nullable=False)
    pickup_street = db.Column(db.String(50), nullable=False)
    pickup_detailed_address = db.Column(db.String(200), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }
    
    @staticmethod
    def create_customer(username, email, phone, password, customer_type, 
                       pickup_district, pickup_name, pickup_house, pickup_street, 
                       pickup_detailed_address, business_name=None):
        customer = Customer(
            username=username,
            email=email,
            phone=phone,
            customer_type=customer_type,
            business_name=business_name,
            pickup_district=pickup_district,
            pickup_name=pickup_name,
            pickup_house=pickup_house,
            pickup_street=pickup_street,
            pickup_detailed_address=pickup_detailed_address
        )
        customer.set_password(password)
        return customer

class Admin(User):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
    
    @staticmethod
    def create_admin(username, email, password, phone):
        admin = Admin(
            username=username,
            email=email,
            phone=phone
        )
        admin.set_password(password)
        return admin
