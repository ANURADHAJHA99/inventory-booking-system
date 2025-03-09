import csv
import click
from datetime import datetime
from flask.cli import with_appcontext
from app import db
from app.models.member import MemberModel
from app.models.inventory_item import InventoryItemModel
from app.repositories.member_repository import MemberRepository
from app.repositories.inventory_repository import InventoryRepository
from app.domain.member import Member
from app.domain.inventory_item import InventoryItem

@click.command('import-csv')
@click.option('--members', help='Path to members.csv file')
@click.option('--inventory', help='Path to inventory.csv file')
@with_appcontext
def import_csv(members, inventory):
    """Import data from members.csv and inventory.csv files"""
    if members:
        import_members(members)
    
    if inventory:
        import_inventory(inventory)
    
    if not members and not inventory:
        click.echo('No file path provided. Use --members or --inventory options.')

def import_members(file_path):
    """Import members from a CSV file"""
    try:
        member_repository = MemberRepository.get_instance()
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 0
            
            # Clear existing members
            db.session.query(MemberModel).delete()
            
            for row in reader:
                # Parse date joined
                date_joined = datetime.fromisoformat(row['date_joined'])
                
                # Create member domain object
                member = Member(
                    id=None,  # ID will be assigned by the database
                    name=row['name'],
                    surname=row['surname'],
                    booking_count=int(row['booking_count']),
                    date_joined=date_joined
                )
                
                # Use repository to create member
                member_repository.create(member)
                counter += 1
            
            click.echo(f'Successfully imported {counter} members')
    
    except Exception as e:
        click.echo(f'Error importing members: {str(e)}')
        db.session.rollback()

def import_inventory(file_path):
    """Import inventory items from a CSV file"""
    try:
        inventory_repository = InventoryRepository.get_instance()
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 0
            
            # Clear existing inventory
            db.session.query(InventoryItemModel).delete()
            
            for row in reader:
                # Parse expiration date (DD/MM/YYYY)
                expiration_date_str = row['expiration_date']
                day, month, year = map(int, expiration_date_str.split('/'))
                expiration_date = datetime(year, month, day).date()
                
                # Create inventory item domain object
                item = InventoryItem(
                    id=None,  # ID will be assigned by the database
                    title=row['title'],
                    description=row['description'],
                    remaining_count=int(row['remaining_count']),
                    expiration_date=expiration_date
                )
                
                # Use repository to create inventory item
                inventory_repository.create(item)
                counter += 1
            
            click.echo(f'Successfully imported {counter} inventory items')
    
    except Exception as e:
        click.echo(f'Error importing inventory: {str(e)}')
        db.session.rollback()