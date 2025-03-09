from datetime import date

class InventoryItem:
    """Inventory item domain entity"""
    
    def __init__(self, id, title, description, remaining_count, expiration_date):
        self.id = id
        self.title = title
        self.description = description
        self.remaining_count = remaining_count
        self.expiration_date = expiration_date
    
    def is_available(self):
        """Check if the item is available for booking"""
        return self.remaining_count > 0
    
    def is_expired(self):
        """Check if the item has expired"""
        return self.expiration_date < date.today()
    
    def __repr__(self):
        return f"<InventoryItem {self.title}>"