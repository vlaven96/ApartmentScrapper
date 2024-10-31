from flask import Blueprint, render_template
from models.models import Apartment, Configuration

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    apartments = Apartment.query.all()
    configurations = Configuration.query.all()
    return render_template('index.html', apartments=apartments, configurations=configurations)
