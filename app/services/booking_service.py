# app/services/booking_service.py
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

from app.repositories.member_repository import MemberRepository
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.booking_repository import BookingRepository
from app.domain.member import Member
from app.domain.inventory_item import InventoryItem
from app.domain.booking import Booking
from app.constants import MAX_BOOKINGS

class BookingService:
    """Service for booking-related business logic using singleton pattern"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(
                MemberRepository.get_instance(),
                InventoryRepository.get_instance(),
                BookingRepository.get_instance()
            )
        return cls._instance
    
    def __init__(
        self, 
        member_repository: MemberRepository,
        inventory_repository: InventoryRepository, 
        booking_repository: BookingRepository
    ):
        """
        Initialize the booking service with repositories.
        
        Args:
            member_repository: Repository for member data access
            inventory_repository: Repository for inventory data access
            booking_repository: Repository for booking data access
        """
        self.member_repository = member_repository
        self.inventory_repository = inventory_repository
        self.booking_repository = booking_repository
        self.max_bookings: int = MAX_BOOKINGS
    
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