from app.constants import MAX_BOOKINGS

class Member:
    """Member domain entity"""
    
    def __init__(self, id, name, surname, booking_count, date_joined):
        self.id = id
        self.name = name
        self.surname = surname
        self.booking_count = booking_count
        self.date_joined = date_joined
    
    def can_book(self, max_bookings=MAX_BOOKINGS):
        """Check if the member can make more bookings"""
        return self.booking_count < max_bookings
    
    def full_name(self):
        """Get the full name of the member"""
        return f"{self.name} {self.surname}"
    
    def __repr__(self):
        return f"<Member {self.full_name()}>"