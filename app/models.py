from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()

# Association Table for Many-to-Many Relationship
user_groups = db.Table(
    'user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    mobile_number = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    groups = db.relationship('Group', secondary=user_groups, back_populates='users')
    bookings = relationship('DestinationBooking', back_populates='user')
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
      
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    # Flask-Login required properties
    @property
    def is_active(self):
        # Assuming all users are active; modify if you have an `active` column
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_groups, back_populates='groups')

    def __repr__(self):
        return f'<Group {self.name}>'

class Destination(db.Model):
    __tablename__ = 'destination'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    main_image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(80),nullable=False)
    price = db.Column(db.String(80), nullable=False)
    days = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.String(120),  nullable=False)
    description = db.Column(db.String(500), nullable=False)
    destination = db.Column(db.String(80),  nullable=False)
    language = db.Column(db.String(80), nullable=False)
    currency_type = db.Column(db.String(80), nullable=False)
    sub_title = db.Column(db.String(80),  nullable=False)
    sub_description = db.Column(db.String(300), nullable=False)
    sub_image = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Adding the relationship for Galleries associated with this Destination
    galleries = db.relationship('Gallery', backref='destination', lazy=True)

    bookings = relationship('DestinationBooking', back_populates='destination')
    def __repr__(self):
        return f'{self.title}'


class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    
    image1 = db.Column(db.String(255), nullable=False)
    image2 = db.Column(db.String(255), nullable=False)
    image3 = db.Column(db.String(255), nullable=False)
    image4 = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'{self.destination_id}'
    

class DestinationBooking(db.Model):
    __tablename__ = 'destination_booking'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Booking Details
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    no_of_persons = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(255), default='Pendding')
    # Relationships
    destination = relationship('Destination', back_populates='bookings')
    user = relationship('User', back_populates='bookings')

    @classmethod
    def check_existing_booking(cls, user_id, destination_id, from_date, to_date):
        existing_booking = cls.query.filter(
            cls.user_id == user_id,
            cls.destination_id == destination_id,
            cls.from_date <= to_date,
            cls.to_date >= from_date
        ).first()
        return existing_booking is not None

    def __repr__(self):
        return f'{self.user.username}' 