from app import db
from app.models.member import MemberModel
from app.domain.member import Member
from typing import Optional

class MemberRepository:
    """Repository for member data access"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_by_id(self, member_id: int) -> Optional[Member]:
        """Get a member by ID"""
        member = MemberModel.query.get(member_id)
        if not member:
            return None
        
        return Member(
            id=member.id,
            name=member.name,
            surname=member.surname,
            booking_count=member.booking_count,
            date_joined=member.date_joined
        )
    
    def get_by_name_and_surname(self, name: str, surname: str) -> Optional[Member]:
        """Get a member by name and surname"""
        member = MemberModel.query.filter_by(name=name, surname=surname).first()
        if not member:
            return None
        
        return Member(
            id=member.id,
            name=member.name,
            surname=member.surname,
            booking_count=member.booking_count,
            date_joined=member.date_joined
        )
    
    def increment_booking_count(self, member_id: int) -> bool:
        """Increment the booking count for a member"""
        member = MemberModel.query.get(member_id)
        if not member:
            return False
        
        member.booking_count += 1
        db.session.commit()
        return True
    
    def decrement_booking_count(self, member_id: int) -> bool:
        """Decrement the booking count for a member"""
        member = MemberModel.query.get(member_id)
        if not member or member.booking_count <= 0:
            return False
        
        member.booking_count -= 1
        db.session.commit()
        return True
    
    def create(self, member: Member) -> Member:
        """Create a new member"""
        new_member = MemberModel(
            name=member.name,
            surname=member.surname,
            booking_count=member.booking_count,
            date_joined=member.date_joined
        )
        
        db.session.add(new_member)
        db.session.commit()
        
        return Member(
            id=new_member.id,
            name=new_member.name,
            surname=new_member.surname,
            booking_count=new_member.booking_count,
            date_joined=new_member.date_joined
        )