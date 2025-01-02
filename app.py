from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from models.database import db
from models.user import User
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__, 
                template_folder='views/templates',
                static_folder='views/static',
                static_url_path='')
    

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///fastx.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    db.init_app(app)
    migrate = Migrate(app, db)
    


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():

        from controllers.auth_controller import auth_bp
        from controllers.dashboard_controller import dashboard_bp
        from controllers.parcel_controller import parcel_bp
        from controllers.admin_controller import admin_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(parcel_bp)
        app.register_blueprint(admin_bp)
        

        db.create_all()
        

        admin = Admin.query.filter_by(email='shehzadhakim799@gmail.com').first()
        if not admin:
            admin = Admin.create_admin(
                username='FastX ADMIN',
                email='shehzadhakim799@gmail.com',
                password='shehzadhakim@@@',
                phone='+8801234567890'
            )
            db.session.add(admin)
            db.session.commit()
    
from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_migrate import Migrate
from models.database import db
from models.user import User, Admin
from models.parcel import Parcel
import os

app = Flask(__name__, template_folder='views/templates', static_folder='views/static', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'fastx.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    

    admin = Admin.query.filter_by(email='shehzadhakim799@gmail.com').first()
    if not admin:
        admin = Admin.create_admin(
            username='FastX ADMIN',
            email='shehzadhakim799@gmail.com',
            password='shehzadhakim@@@',
            phone='+8801234567890'
        )
        db.session.add(admin)
        db.session.commit()
    
    from controllers.auth_controller import auth_bp
    from controllers.dashboard_controller import dashboard_bp
    from controllers.parcel_controller import parcel_bp
    from controllers.admin_controller import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(parcel_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
