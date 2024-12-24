from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, bcrypt  # Import `db` and `bcrypt` from models
from .views import main
from werkzeug.exceptions import RequestEntityTooLarge
import os
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app = Flask(__name__, static_folder='static')  # Add static_folder config here
    
    # Load configuration
    app.register_blueprint(main) 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discover_destinations.db'  # Use a proper config for production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey12345'
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

    # Configuring upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/images')



    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    


    with app.app_context():
        from . import views  # Import views to register routes
        # Ensure all models are imported in `models.py` for migrations
        # Avoid db.create_all() if using migrations

    return app
