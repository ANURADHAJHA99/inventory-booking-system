import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models.member import MemberModel
from app.models.inventory_item import InventoryItemModel
from app.models.booking import BookingModel

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

class MemberModelTestCase(BaseTestCase):
    def test_member_creation(self):
        member = MemberModel(
            name='Test',
            surname='User',
            booking_count=0,
            date_joined=datetime.utcnow()
        )
        db.session.add(member)
        db.session.commit()
        
        self.assertEqual(member.name, 'Test')
        self.assertEqual(member.surname, 'User')
        self.assertEqual(member.booking_count, 0)