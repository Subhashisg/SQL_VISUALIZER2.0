from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, encrypt_data, decrypt_data

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with API keys
    api_keys = db.relationship('APIKey', backref='user', lazy=True, cascade='all, delete-orphan')
    sql_queries = db.relationship('SQLQuery', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_gemini_api_key(self):
        api_key_record = APIKey.query.filter_by(user_id=self.id, service='gemini').first()
        if api_key_record:
            return decrypt_data(api_key_record.encrypted_key)
        return None
    
    def set_gemini_api_key(self, api_key):
        # Remove existing key if any
        existing_key = APIKey.query.filter_by(user_id=self.id, service='gemini').first()
        if existing_key:
            db.session.delete(existing_key)
        
        # Add new encrypted key
        new_key = APIKey(
            user_id=self.id,
            service='gemini',
            encrypted_key=encrypt_data(api_key)
        )
        db.session.add(new_key)
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service = db.Column(db.String(50), nullable=False)  # 'gemini', 'openai', etc.
    encrypted_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<APIKey {self.service} for User {self.user_id}>'

class SQLQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query_text = db.Column(db.Text, nullable=False)
    query_type = db.Column(db.String(50))  # SELECT, INSERT, UPDATE, DELETE, CREATE, etc.
    execution_time = db.Column(db.Float)  # in seconds
    result_count = db.Column(db.Integer)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # JSON field to store query results for visualization
    result_data = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<SQLQuery {self.id} by User {self.user_id}>'

class GeneratedTable(db.Model):
    """Track AI-generated tables and their schemas"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    table_name = db.Column(db.String(100), nullable=False)
    table_schema = db.Column(db.JSON, nullable=False)  # Store column definitions
    sample_data_count = db.Column(db.Integer, default=0)
    created_by_ai = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GeneratedTable {self.table_name} for User {self.user_id}>'
