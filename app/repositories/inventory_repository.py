from app import db
from app.models.inventory_item import InventoryItemModel
from app.domain.inventory_item import InventoryItem

class InventoryRepository:
    """Repository for inventory item data access"""
    
    def get_by_id(self, item_id):
        """Get an inventory item by ID"""
        item = InventoryItemModel.query.get(item_id)
        if not item:
            return None
        
        return InventoryItem(
            id=item.id,
            title=item.title,
            description=item.description,
            remaining_count=item.remaining_count,
            expiration_date=item.expiration_date
        )
    
    def get_by_title(self, title):
        """Get an inventory item by title"""
        item = InventoryItemModel.query.filter_by(title=title).first()
        if not item:
            return None
        
        return InventoryItem(
            id=item.id,
            title=item.title,
            description=item.description,
            remaining_count=item.remaining_count,
            expiration_date=item.expiration_date
        )
    
    def decrease_quantity(self, item_id):
        """Decrease the remaining count for an inventory item"""
        item = InventoryItemModel.query.get(item_id)
        if not item or item.remaining_count <= 0:
            return False
        
        item.remaining_count -= 1
        db.session.commit()
        return True
    
    def increase_quantity(self, item_id):
        """Increase the remaining count for an inventory item"""
        item = InventoryItemModel.query.get(item_id)
        if not item:
            return False
        
        item.remaining_count += 1
        db.session.commit()
        return True
    
    def create(self, item):
        """Create a new inventory item"""
        new_item = InventoryItemModel(
            title=item.title,
            description=item.description,
            remaining_count=item.remaining_count,
            expiration_date=item.expiration_date
        )
        
        db.session.add(new_item)
        db.session.commit()
        
        return InventoryItem(
            id=new_item.id,
            title=new_item.title,
            description=new_item.description,
            remaining_count=new_item.remaining_count,
            expiration_date=new_item.expiration_date
        )