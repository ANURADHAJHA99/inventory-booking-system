from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from app.repositories.member_repository import MemberRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.booking_repository import BookingRepository
from app.domain.member import Member
from app.domain.inventory_item import InventoryItem
from app.domain.booking import Booking
from app.config import Config

class BookingService:
    """Service for booking-related business logic"""
    
    def __init__(
        self, 
        member_repository: MemberRepository = None,
        inventory_repository: InventoryRepository = None, 
        booking_repository: BookingRepository = None
    ):
        self.member_repository = member_repository or MemberRepository()
        self.inventory_repository = inventory_repository or InventoryRepository()
        self.booking_repository = booking_repository or BookingRepository()
        self.max_bookings: int = Config.MAX_BOOKINGS
    
    def book_item(self, member_id: int, item_title: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Book an inventory item for a member
        
        Args:
            member_id: ID of the member making the booking
            item_title: Title of the inventory item to book
            
        Returns:
            tuple: (booking_data, error_message)
                If successful, booking_data contains the booking details and error_message is None
                If unsuccessful, booking_data is None and error_message contains the error
        """
        # Check if member exists
        member: Optional[Member] = self.member_repository.get_by_id(member_id)
        if not member:
            return None, "Member not found"
        
        # Check if member has reached maximum bookings
        if not member.can_book(self.max_bookings):
            return None, f"Member has reached maximum number of bookings ({self.max_bookings})"
        
        # Check if inventory item exists
        inventory_item: Optional[InventoryItem] = self.inventory_repository.get_by_title(item_title)
        if not inventory_item:
            return None, "Inventory item not found"
        
        # Check if inventory item is available
        if not inventory_item.is_available():
            return None, "Inventory item is not available"
        
        # Check if inventory item has expired
        if inventory_item.is_expired():
            return None, "Inventory item has expired"
        
        # Create the booking
        booking: Optional[Booking] = self.booking_repository.create(member.id, inventory_item.id)
        if not booking:
            return None, "Failed to create booking"
        
        # Update inventory and member
        self.inventory_repository.decrease_quantity(inventory_item.id)
        self.member_repository.increment_booking_count(member.id)
        
        # Return booking details
        return {
            "booking_reference": booking.booking_reference,
            "member_name": member.full_name(),
            "item_title": inventory_item.title,
            "booking_date": booking.booking_date.isoformat()
        }, None
    
    def cancel_booking(self, booking_reference: str) -> Tuple[bool, Optional[str]]:
        """
        Cancel a booking
        
        Args:
            booking_reference: Reference of the booking to cancel
            
        Returns:
            tuple: (success, error_message)
                If successful, success is True and error_message is None
                If unsuccessful, success is False and error_message contains the error
        """
        # Check if booking exists
        booking: Optional[Booking] = self.booking_repository.get_by_reference(booking_reference)
        if not booking:
            return False, "Booking not found"
        
        # Check if booking is already cancelled
        if not booking.is_active:
            return False, "Booking is already cancelled"
        
        # Cancel the booking
        cancelled_booking: Optional[Booking] = self.booking_repository.cancel(booking_reference)
        if not cancelled_booking:
            return False, "Failed to cancel booking"
        
        # Update inventory and member
        self.inventory_repository.increase_quantity(booking.inventory_item_id)
        self.member_repository.decrement_booking_count(booking.member_id)
        
        return True, None