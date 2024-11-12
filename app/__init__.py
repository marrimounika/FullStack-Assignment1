import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_mail import Mail
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    
    # App configuration
    app.config.from_object('config.Config')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

    # Initialize Extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    mail.init_app(app)

    # Set the login view for @login_required
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Import and Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.exchanges import exchanges_bp
    from app.routes.transactions import transactions_bp
    from app.routes.messages import messages_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(exchanges_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(profile_bp)

    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app
