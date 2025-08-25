from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sql_visualizer.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

# Encryption utilities
def get_encryption_key():
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        # Generate a new key if not exists
        key = Fernet.generate_key().decode()
        print(f"Generated new encryption key: {key}")
        print("Please add this to your .env file as ENCRYPTION_KEY")
    return key.encode() if isinstance(key, str) else key

def encrypt_data(data):
    if not data:
        return None
    f = Fernet(get_encryption_key())
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return None
    f = Fernet(get_encryption_key())
    return f.decrypt(encrypted_data.encode()).decode()
