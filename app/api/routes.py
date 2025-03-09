from flask import request, jsonify
from typing import List, Dict, Any, Optional

from app.api import bp
from app.services.booking_service import BookingService
from app.models.inventory_item import InventoryItemModel
from app.models.booking import BookingModel

# Get the singleton instance of BookingService
booking_service = BookingService.get_instance()

@bp.route('/book', methods=['POST']) 
def book_item():
    """
    Book an inventory item
    
    Request body:
    {
        "member_id": integer,
        "item_title": string
    }
    
    Returns:
        201: Booking created successfully
        400: Bad request, error message provided
    """
    data = request.get_json() or {}
    
    # Validate required fields
    if 'member_id' not in data or 'item_title' not in data:
        return jsonify({'error': 'Must include member_id and item_title fields'}), 400
    
    try:
        # Convert member_id to integer
        member_id = int(data['member_id'])
        item_title = str(data['item_title'])
        
        # Book the item using the singleton instance
        booking_data, error = booking_service.book_item(member_id, item_title)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify(booking_data), 201
    except ValueError:
        return jsonify({'error': 'member_id must be an integer'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@bp.route('/cancel', methods=['POST']) 
def cancel_booking():
    """
    Cancel a booking
    
    Request body:
    {
        "booking_reference": string
    }
    
    Returns:
        200: Booking cancelled successfully
        400: Bad request, error message provided
    """
    data = request.get_json() or {}
    
    # Validate required fields
    if 'booking_reference' not in data:
        return jsonify({'error': 'Must include booking_reference field'}), 400
    
    try:
        booking_reference = str(data['booking_reference'])
        
        # Cancel the booking using the singleton instance
        success, error = booking_service.cancel_booking(booking_reference)
        
        if not success:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': f"Booking {booking_reference} cancelled successfully"}), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@bp.route('/inventory', methods=['GET'])
def get_inventory():
    """
    Get all available inventory items
    
    Returns:
        200: List of inventory items
    """
    try:
        items = InventoryItemModel.query.all()
        
        result: List[Dict[str, Any]] = []
        for item in items:
            result.append({
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'remaining_count': item.remaining_count,
                'expiration_date': item.expiration_date.isoformat()
            })
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@bp.route('/members/<int:member_id>/bookings', methods=['GET'])
def get_member_bookings(member_id: int):
    """
    Get all bookings for a member
    
    Args:
        member_id: ID of the member
        
    Returns:
        200: List of bookings for the member
        404: Member not found
    """
    try:
        # Use the singleton instance
        member = booking_service.member_repository.get_by_id(member_id)
        
        if not member:
            return jsonify({'error': 'Member not found'}), 404
        
        bookings = BookingModel.query.filter_by(
            member_id=member_id,
            is_active=True
        ).all()
        
        result: List[Dict[str, Any]] = []
        for booking in bookings:
            result.append({
                'booking_reference': booking.booking_reference,
                'inventory_item_id': booking.inventory_item_id,
                'booking_date': booking.booking_date.isoformat()
            })
        
        return jsonify(result), 200
    except ValueError:
        return jsonify({'error': 'member_id must be an integer'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500