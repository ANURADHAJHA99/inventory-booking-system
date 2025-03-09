from app import db

class InventoryItemModel(db.Model):
    """Inventory item SQLAlchemy model"""
    
    __tablename__ = 'inventory_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    remaining_count = db.Column(db.Integer, default=0)
    expiration_date = db.Column(db.Date, nullable=False)
    
    # Relationship with bookings
    bookings = db.relationship('BookingModel', backref='inventory_item', lazy='dynamic')
    
    def __repr__(self):
        return f"<InventoryItemModel {self.title}>"