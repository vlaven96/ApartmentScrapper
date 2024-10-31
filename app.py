from flask import Flask
from models.models import db
import config
from controllers.apartment_controller import apartment_bp
from controllers.config_controller import config_bp
from controllers.main_controller import main_bp
app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

# Initialize database tables if they don’t exist
with app.app_context():
    db.create_all()

# Register Blueprints
app.register_blueprint(main_bp)  # Register the main blueprint
app.register_blueprint(apartment_bp, url_prefix='/apartments')
app.register_blueprint(config_bp, url_prefix='/configs')

if __name__ == '__main__':
    app.run(debug=True)
