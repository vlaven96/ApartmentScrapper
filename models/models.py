from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120))
    description = db.Column(db.Text)
    url = db.Column(db.String(200))
    rooms = db.Column(db.Integer)
    seen = db.Column(db.Boolean, default=False)
    liked = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)
    floor = db.Column(db.String(50))
    square_meters = db.Column(db.Float)
    price_sqr_meters = db.Column(db.Float)
    build_year = db.Column(db.Integer)

    ingested_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)

    configuration_id = db.Column(db.Integer, db.ForeignKey("configurations.id"), nullable=False)

class Configuration(db.Model):
    __tablename__ = 'configurations'
    id = db.Column(db.Integer, primary_key=True)
    selected_sites = db.Column(db.String(50))
    city = db.Column(db.String(50))
    rooms = db.Column(db.Integer)
    compartment = db.Column(db.String(50))
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    min_square_meters = db.Column(db.Integer)
    max_square_meters = db.Column(db.Integer)
    min_year_built = db.Column(db.Integer)
    exclude_words = db.Column(db.String(200))
    include_words = db.Column(db.String(200))

    apartments = db.relationship("Apartment", backref="configuration", lazy=True)