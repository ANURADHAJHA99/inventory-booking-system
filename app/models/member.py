from app import db
from datetime import datetime

class MemberModel(db.Model):
    """Member SQLAlchemy model"""
    
    __tablename__ = 'members'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    booking_count = db.Column(db.Integer, default=0)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with bookings
    bookings = db.relationship('BookingModel', backref='member', lazy='dynamic')
    
    def __repr__(self):
        return f"<MemberModel {self.name} {self.surname}>"