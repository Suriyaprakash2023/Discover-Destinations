from flask import Blueprint, render_template,jsonify, request, redirect, url_for, flash, session
from .models import *
from werkzeug.security import generate_password_hash
from flask_restful import Resource, Api

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
    return render_template('destination.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        print(request.data)
        username = request.json.get('username')
        email = request.json.get('email')
        mobile_number = request.json.get('mobile_number')
        password = request.json.get('password')

        # Check for existing user
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            return render_template('register.html')

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Create and save new user
        new_user = User(username=username, email=email, password=hashed_password)
        new_user.mobile_number = mobile_number
        new_user.groups = 'user'
        db.session.add(new_user)
        db.session.commit()
        # Respond with success message
        return render_template('login.html')
    return render_template('register.html')

@main.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        mobile_number = request.form.get('mobile_number')
        password = request.form.get('password')

        # Query for the user by email
        user = User.query.filter_by(mobile_number=mobile_number).first()

        if user and user.check_password(password):
            print(user.groups,"user.groups")
            if any(group.name == 'admin' for group in user.groups):
                session['user_id'] = user.id  # Store the user's ID in the session (indicating they are logged in)
                flash('Login successful!', 'success')

                return redirect(url_for('main.dashboard'))  # Redirect to a protected page (e.g., dashboard)
            else :
                session['user_id'] = user.id  # Store the user's ID in the session (indicating they are logged in)
                flash('Login successful!', 'success')
                print('user')
                return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@main.route('/dashboard')
def dashboard():
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))  # Redirect to login if not logged in
    # user = User.query.get(session['user_id'])

    return render_template('dashboard/dashboard_index.html')

@main.route('/bookings')
def bookings():

    return render_template('dashboard/booking.html')

@main.route('/listing')
def listing():

    return render_template('dashboard/listing.html')

@main.route('/addtour',methods=['POST','GET'])
def addtour():
    if request.method == 'POST':
        title = request.form.get('title')
        main_image = request.form.get('main_image')
        category = request.form.get('category') 
        rating = request.form.get('rating') 
        description = request.form.get('description') 
        price = request.form.get('price') 
        destination = request.form.get('destination_place') 
        currency_type = request.form.get('currency') 
        language = request.form.get('language') 
        sub_title = request.form.get('sub_title') 
        sub_description = request.form.get('sub_description') 
        sub_image = request.form.get('sub_image') 

        print(language,"language")
        create_destination = Destination(
            title=title,
            main_image=main_image,
            category=category,
            price=price,
            rating=rating,
            destination=destination,
            description=description,
            currency_type=currency_type,
            language=language,
            sub_title=sub_title,
            sub_description=sub_description,
            sub_image=sub_image
        )

        # Add the destination to the session and commit
        # db.session.add(create_destination)
        # db.session.commit()

        image1 = request.form.get('image1') 
        image2 = request.form.get('image2') 
        image3 = request.form.get('image3') 
        image4 = request.form.get('image4') 
        print(image1,image2,image3,image4 )
        # Create a gallery and associate it with the destination
        gallery = Gallery(
            destination_id=destination.id,  # Associate with the created destination
            image1=image1,
            image2=image2,
            image3=image3,
            image4=image4
        )

        # # Add the gallery to the session and commit
        db.session.add(gallery)
        db.session.commit()
        return redirect(url_for('main.listing'))
    return render_template('dashboard/addtour.html')


@main.route('/logout')
def logout():
    # Remove the user from the session to log them out
    session.pop('user_id', None)  # This will remove the 'user' from the session
    return redirect(url_for('main.index'))  # Redirect to home page after logout
