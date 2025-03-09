from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register CLI commands
    from app.commands import register_commands
    register_commands(app)
    
    @app.route('/')
    def index():
        return {
            "message": "Inventory Booking System API",
            "endpoints": {
                "book_item": "/api/book",
                "cancel_booking": "/api/cancel",
                "get_inventory": "/api/inventory",
                "get_member_bookings": "/api/members/<member_id>/bookings"
            }
        }
    
    return app

# Import models to ensure they are registered with SQLAlchemy
from app.models import member, inventory_item, booking