from flask import Blueprint, render_template
# from .models import ExampleModel

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
