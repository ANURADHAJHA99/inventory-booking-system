import uuid
from datetime import datetime

class Booking:
    """Booking domain entity"""
    
    def __init__(self, id, booking_reference, member_id, inventory_item_id, booking_date=None, is_active=True):
        self.id = id
        self.booking_reference = booking_reference
        self.member_id = member_id
        self.inventory_item_id = inventory_item_id
        self.booking_date = booking_date or datetime.now()
        self.is_active = is_active
    
    @staticmethod
    def generate_reference():
        """Generate a unique booking reference"""
        return str(uuid.uuid4())[:8].upper()
    
    def __repr__(self):
        return f"<Booking {self.booking_reference}>"