from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from models.database import db
from models.user import User, Admin

def create_app():

    app = Flask(__name__,
                template_folder='views/templates',
                static_folder='views/static',
                static_url_path='')
    

    app.config['SECRET_KEY'] = 'your-secret-key' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastx.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    

    db.init_app(app)
    

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():

        db.create_all()
        
   
        Admin.create_admin()
        
     
        from controllers.auth_controller import auth_bp
        app.register_blueprint(auth_bp)  
        

        @app.route('/')
        def index():
            if current_user.is_authenticated:
                return redirect(url_for('dashboard'))
            return redirect(url_for('auth.login'))
        
        @app.route('/dashboard')
        @login_required
        def dashboard():
            return "Dashboard banano hoy nai ekhono"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
