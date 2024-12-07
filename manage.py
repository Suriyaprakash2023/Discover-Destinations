from app import create_app, db
from flask_login import LoginManager
from app.models import User
app = create_app()

# Initialize the LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to this view if not logged in

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Query the user by ID

if __name__ == '__main__':
    app.run(debug=True, port=8989)  # Start the app
