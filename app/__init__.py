from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, bcrypt  # Import `db` and `bcrypt` from models
from .views import main
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.register_blueprint(main) 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discover_destinations.db'  # Use a proper config for production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey12345'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from . import views  # Import views to register routes
        # Ensure all models are imported in `models.py` for migrations
        # Avoid db.create_all() if using migrations

    return app
