from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db, bcrypt  # Import `db` and `bcrypt` from models
from .views import main
from werkzeug.exceptions import RequestEntityTooLarge
import os
migrate = Migrate()

def create_app():

    # Initialize Flask with proper static folder configuration
    app = Flask(__name__, static_folder='static',static_url_path='/static')
    
    # Load configuration
    app.register_blueprint(main)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///discover_destinations.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey12345'
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

    # Better path handling for upload folder
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(CURRENT_DIR, 'static/images')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)



    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    


    with app.app_context():
        from . import views  # Import views to register routes
        # Ensure all models are imported in `models.py` for migrations
        # Avoid db.create_all() if using migrations

    return app
