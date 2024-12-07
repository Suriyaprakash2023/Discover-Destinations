from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash

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
    rating = db.Column(db.String(120),  nullable=False)
    description = db.Column(db.String(500), nullable=False)
    destination = db.Column(db.String(80),  nullable=False)
    language = db.Column(db.String(80), nullable=False)
    currency_type = db.Column(db.String(80), nullable=False)
    sub_title = db.Column(db.String(80),  nullable=False)
    sub_description = db.Column(db.String(300), nullable=False)
    sub_image = db.Column(db.String(255), nullable=False)

    # Adding the relationship for Galleries associated with this Destination
    galleries = db.relationship('Gallery', backref='destination', lazy=True)

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