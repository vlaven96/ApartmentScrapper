from flask import Blueprint, render_template, jsonify, redirect, url_for
from models.models import db, Apartment
from services.scrapers.scraper_service import scrape_apartments

apartment_bp = Blueprint('apartment', __name__)

@apartment_bp.route('/apartments', methods=['GET'])
def list_apartments():
    apartments = Apartment.query.all()
    return render_template('index.html', apartments=apartments)

@apartment_bp.route('/apartments/<int:id>', methods=['GET'])
def apartment_detail(id):
    apartment = Apartment.query.get_or_404(id)
    return render_template('detail.html', apartment=apartment)

@apartment_bp.route('/apartments/<int:id>/seen', methods=['PATCH'])
def mark_seen(id):
    apartment = Apartment.query.get_or_404(id)
    apartment.seen = True
    db.session.commit()
    return jsonify({'message': 'Apartment marked as seen', 'id': apartment.id, 'seen': apartment.seen}), 200

@apartment_bp.route('/apartments/<int:id>/loved', methods=['PATCH'])
def mark_loved(id):
    apartment = Apartment.query.get_or_404(id)
    apartment.loved = True
    db.session.commit()
    return jsonify({'message': 'Apartment marked as loved', 'id': apartment.id, 'loved': apartment.loved}), 200

@apartment_bp.route('/scrape', methods=['POST'])
def scrape():
    scrape_apartments()  # Run the scraping function
    return redirect(url_for('apartment.list_apartments'))  # Redirect back to apartments listing after scraping
