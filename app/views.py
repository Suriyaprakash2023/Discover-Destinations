from flask import Blueprint, render_template,jsonify, request, redirect, url_for, flash, session,current_app
from .models import *
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    
    # items = ExampleModel.query.all()
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/destination')
def destination():
    destinations = Destination.query.order_by(Destination.created_at.desc()).all()
    for dest in destinations:
        dest.rating = int(dest.rating)  # Convert string to integer
    return render_template('destination.html',destinations=destinations)

@main.route('/destination/<int:id>')
def destination_detail(id):
    print(current_user.username,"user")
    destination = Destination.query.get_or_404(id)

    return render_template('destination_detail.html',destination=destination)



@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/register', methods=['GET',"POST"])
def register():
    print(request.data,"data")
    if request.method == 'POST':
        
        username = request.form.get('username')
        email = request.form.get('email')
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')
        # Check for existing user
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('UserName Or Email Already Registered..!', 'error')
            return redirect(url_for('main.register')) 

        # Hash the password before saving
        # hashed_password = generate_password_hash(password)

        user_group = Group.query.filter_by(name="user").first()
        print(user_group,"user_group")
        # Create and save new user
        new_user = User(username=username, email=email, password=password)
        new_user.mobile_number = mobile_number
        new_user.groups.append(user_group)
        db.session.add(new_user)
        db.session.commit()
        # Respond with success message
        flash('Login successful!', 'success')
        return render_template('login.html')
    return render_template('register.html')

@main.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')
        print(mobile_number,password,"mob and pass")
        # Query for the user by email
        user = User.query.filter_by(mobile_number=mobile_number).first()
        
        if user and user.check_password(password):
            print(user.groups,"user.groups")
            if any(group.name == 'admin' for group in user.groups):
                
                login_user(user)  # Log in the user
                session['user_id'] = user.id  # Store the user's ID in the session (indicating they are logged in)
                flash('Login successful!', 'success')
                print("admin")
                return redirect(url_for('main.dashboard'))  # Redirect to a protected page (e.g., dashboard)
            else :
                login_user(user)  # Log in the user
                session['user_id'] = user.id  # Store the user's ID in the session (indicating they are logged in)
                flash('Login successful!', 'success')
                print('user')
                return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))  # Redirect to login if not logged in
    # user = User.query.get(session['user_id'])
    destination_count = Destination.query.count()

    current_date = datetime.utcnow()
    # Calculate the date 3 days ago
    three_days_ago = current_date - timedelta(days=3)
    # Query to count the number of destinations added in the last 3 days
    recent_destination_count = Destination.query.filter(Destination.created_at >= three_days_ago).count()

    return render_template('dashboard/dashboard_index.html',destination_count=destination_count,recent_destination_count=recent_destination_count)

@main.route('/bookings')
def bookings():

    return render_template('dashboard/booking.html')

@main.route('/listing')
def listing():
    
    destinations = Destination.query.all()
    return render_template('dashboard/listing.html', destinations=destinations)



def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, folder):
    """
    Save uploaded image and return a unique filename.
    
    :param file: FileStorage object from Flask
    :param folder: Destination folder for saving the image
    :return: Unique filename or None if saving fails
    """
    if file and allowed_file(file.filename):
        # Generate a unique filename to prevent overwriting
        filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
        
        # Ensure the upload folder exists
        os.makedirs(os.path.join(current_app.root_path, folder), exist_ok=True)
        
        # Save the file
        file_path = os.path.join(current_app.root_path, folder, filename)
        file.save(file_path)
        
        return filename
    return None

@main.route('/addtour', methods=['POST', 'GET'])
def addtour():
    if request.method == 'POST':
        try:
            # Extract form data
            title = request.form.get('title')
            category = request.form.get('category')
            rating = request.form.get('rating')
            description = request.form.get('description')
            price = request.form.get('price')
            days = request.form.get('days')
            destination = request.form.get('destination_place')
            currency_type = request.form.get('currency')
            language = request.form.get('language')
            sub_title = request.form.get('sub_title')
            sub_description = request.form.get('sub_description')
            images = request.files.get('images')
            print(images,"gffdgfhgfhjhg")
            # Handle main image upload
            main_image = request.files.get('main_image')
            main_image_filename = save_image(main_image, 'static/uploads/destinations')

            # Handle sub image upload
            sub_image = request.files.get('sub_image')
         
            sub_image_filename = save_image(sub_image, 'static/uploads/destinations')

            # Create destination object
            create_destination = Destination(
                title=title,
                main_image=main_image_filename,
                category=category,
                price=price,
                days=days,
                rating=rating,
                destination=destination,
                description=description,
                currency_type=currency_type,
                language=language,
                sub_title=sub_title,
                sub_description=sub_description,
                sub_image=sub_image_filename
            )
            
            # Add destination to the database
            db.session.add(create_destination)
            db.session.commit()

            image1 = request.files.get('image1')
            image2 = request.files.get('image2')
            image3 = request.files.get('image3')
            image4 = request.files.get('image4')

            print(image1,image2,image3,image4,"image1")
            image1_filename = save_image(image1, 'static/uploads/gallery')
            image2_filename = save_image(image2, 'static/uploads/gallery')
            image3_filename = save_image(image3, 'static/uploads/gallery')
            image4_filename = save_image(image4, 'static/uploads/gallery')
            print(image1_filename,image2_filename,image3_filename,image4_filename,"image1_filename")
            # Handle gallery images
           
            gallery = Gallery(
                destination_id=create_destination.id,  # Associate with the created destination
                image1=image1_filename,
                image2=image2_filename,
                image3=image3_filename,
                image4=image4_filename
            )


            # Add gallery to the database
            db.session.add(gallery)
            db.session.commit()

            # Flash success message and redirect
            flash(f'{destination} Destination Added Successfully!', 'success')
            return redirect(url_for('main.listing'))

        except Exception as e:
            db.session.rollback()
            print("Exception in addtour:", e)
            flash(f'Error saving to database: {str(e)}', 'error')
            return redirect(url_for('main.addtour'))

    # Render the add tour template for GET requests
    return render_template('dashboard/addtour.html')

def allowed_file(filename):
    """Check if the file has a valid extension."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/edit_tour/<int:id>/', methods=['POST','GET'])
def edit_tour(id):
    destination = Destination.query.get_or_404(id)
    if request.method == 'POST':
        flash(f'Error saving to database', 'error')
        return redirect(url_for('main.edit_tour'))
    
    return render_template('dashboard/edit_tour.html',destination=destination)

@main.route('/logout')
def logout():
    # Remove the user from the session to log them out
    session.pop('user_id', None)  # This will remove the 'user' from the session
    return redirect(url_for('main.index'))  # Redirect to home page after logout


@main.route('/booking')
@login_required
def booking():
    if request.method == 'POST':
        destination_id = request.form.get('destination_id')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        no_of_persons = request.form.get('no_of_persons')
        amount = request.form.get('amount')
        
        print(destination_id,from_date,to_date,no_of_persons,amount,"amount")
        # new_booking = DestinationBooking(
        # destination_id=destination.id,
        # user_id=current_user.id,
        # from_date=datetime(2024, 7, 1),
        # to_date=datetime(2024, 7, 10),
        # no_of_persons=2,
        # amount=1500.00
        # )
        # db.session.add(new_booking)
        # db.session.commit()

        destination = Destination.query.get_or_404(1) #destination_id
        return render_template('destination_detail.html',destination=destination)