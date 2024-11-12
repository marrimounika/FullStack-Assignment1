# app/models.py

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'  # Explicit table name for clarity
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Additional fields can be added here (e.g., profile picture, bio)

    # Relationships
    books = db.relationship('Book', backref='owner', lazy=True)
    sent_exchange_requests = db.relationship('ExchangeRequest', 
                                             foreign_keys='ExchangeRequest.sender_id', 
                                             back_populates='sender', 
                                             lazy=True)
    received_exchange_requests = db.relationship('ExchangeRequest', 
                                                 foreign_keys='ExchangeRequest.receiver_id', 
                                                 back_populates='receiver', 
                                                 lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    profile = db.relationship('Profile', uselist=False, backref='user')  # One-to-one relationship with Profile

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    reading_preferences = db.Column(db.Text, nullable=True)
    favorite_genres = db.Column(db.Text, nullable=True)
    books_wanted = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)  # One-to-one relationship

    def __repr__(self):
        return f"Profile(User ID: {self.user_id})"

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    availability_status = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Additional fields can be added here (e.g., description)

    # Relationships
    exchange_requests = db.relationship('ExchangeRequest', back_populates='book', lazy=True)
    

    def __repr__(self):
        return f"Book('{self.title}', Owner ID: {self.user_id})"

class ExchangeRequest(db.Model):
    __tablename__ = 'exchange_request'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    delivery_method = db.Column(db.String(50), nullable=False)
    exchange_duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # e.g., pending, accepted, rejected
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_exchange_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_exchange_requests')
    book = db.relationship('Book', back_populates='exchange_requests')
    

    def __repr__(self):
        return f"ExchangeRequest(Sender ID: {self.sender_id}, Receiver ID: {self.receiver_id}, Book ID: {self.book_id}, Status: {self.status})"

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Message(From: {self.sender_id}, To: {self.receiver_id}, Read: {self.read})"

class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exchange_request_id = db.Column(db.Integer, db.ForeignKey('exchange_request.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='initiated')  # Possible values: 'initiated', 'completed', 'cancelled'
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    exchange_request = db.relationship('ExchangeRequest', backref='transaction', lazy=True)

    def __repr__(self):
        return f"Transaction(User ID: {self.user_id}, Exchange Request ID: {self.exchange_request_id}, Status: {self.status})"
