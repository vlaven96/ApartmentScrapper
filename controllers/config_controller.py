from flask import Blueprint, render_template, request, redirect, url_for
from models.models import Configuration
from services.config_service import create_configuration
from services.scrapers.scraper_service import scrape_apartments

config_bp = Blueprint('config', __name__)

@config_bp.route('/', methods=['GET'])
def list_configs():
    configurations = Configuration.query.all()
    return render_template('index.html', configurations=configurations)

@config_bp.route('/', methods=['POST'])
def create_config():
    data = request.form
    create_configuration(data)
    return redirect(url_for('config.list_configs'))

@config_bp.route('/<int:config_id>', methods=['GET'])
def config_detail(config_id):
    config = Configuration.query.get_or_404(config_id)
    return render_template('config_detail.html', config=config)

@config_bp.route('/<int:config_id>/scrape', methods=['POST'])
def scrape_with_config(config_id):
    config = Configuration.query.get_or_404(config_id)
    scrape_apartments(config)  # Pass the config to the scraping function
    return redirect(url_for('config.config_detail', config_id=config_id))

@config_bp.route('/new', methods=['GET'])
def new_config():
    return render_template('create_config.html')
