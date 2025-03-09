from app import db
from app.models.booking import BookingModel
from app.domain.booking import Booking

class BookingRepository:
    """Repository for booking data access"""
    
    def get_by_id(self, booking_id):
        """Get a booking by ID"""
        booking = BookingModel.query.get(booking_id)
        if not booking:
            return None
        
        return Booking(
            id=booking.id,
            booking_reference=booking.booking_reference,
            member_id=booking.member_id,
            inventory_item_id=booking.inventory_item_id,
            booking_date=booking.booking_date,
            is_active=booking.is_active
        )
    
    def get_by_reference(self, booking_reference):
        """Get a booking by reference"""
        booking = BookingModel.query.filter_by(booking_reference=booking_reference).first()
        if not booking:
            return None
        
        return Booking(
            id=booking.id,
            booking_reference=booking.booking_reference,
            member_id=booking.member_id,
            inventory_item_id=booking.inventory_item_id,
            booking_date=booking.booking_date,
            is_active=booking.is_active
        )
    
    def create(self, member_id, inventory_item_id):
        """Create a new booking"""
        # Generate a unique booking reference
        booking_reference = Booking.generate_reference()
        
        # Create the booking
        new_booking = BookingModel(
            booking_reference=booking_reference,
            member_id=member_id,
            inventory_item_id=inventory_item_id,
            is_active=True
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return Booking(
            id=new_booking.id,
            booking_reference=new_booking.booking_reference,
            member_id=new_booking.member_id,
            inventory_item_id=new_booking.inventory_item_id,
            booking_date=new_booking.booking_date,
            is_active=new_booking.is_active
        )
    
    def cancel(self, booking_reference):
        """Cancel a booking by reference"""
        booking = BookingModel.query.filter_by(
            booking_reference=booking_reference,
            is_active=True
        ).first()
        
        if not booking:
            return None
        
        booking.is_active = False
        db.session.commit()
        
        return Booking(
            id=booking.id,
            booking_reference=booking.booking_reference,
            member_id=booking.member_id,
            inventory_item_id=booking.inventory_item_id,
            booking_date=booking.booking_date,
            is_active=booking.is_active
        )