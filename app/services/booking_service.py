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