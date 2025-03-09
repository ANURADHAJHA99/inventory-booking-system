from flask import request, jsonify
from app.api import bp
from app.services.booking_service import BookingService

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
    
    # Book the item
    service = BookingService()
    booking_data, error = service.book_item(data['member_id'], data['item_title'])
    
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(booking_data), 201

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
    
    # Cancel the booking
    service = BookingService()
    success, error = service.cancel_booking(data['booking_reference'])
    
    if not success:
        return jsonify({'error': error}), 400
    
    return jsonify({'message': f"Booking {data['booking_reference']} cancelled successfully"}), 200

# Add additional endpoints for listing available inventory and member bookings
@bp.route('/inventory', methods=['GET'])
def get_inventory():
    """Get all available inventory items"""
    from app.repositories.inventory_repository import InventoryRepository
    from app.models.inventory_item import InventoryItemModel
    
    repository = InventoryRepository()
    items = InventoryItemModel.query.all()
    
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'remaining_count': item.remaining_count,
            'expiration_date': item.expiration_date.isoformat()
        })
    
    return jsonify(result), 200

@bp.route('/members/<int:member_id>/bookings', methods=['GET'])
def get_member_bookings(member_id):
    """Get all bookings for a member"""
    from app.repositories.member_repository import MemberRepository
    from app.models.booking import BookingModel
    
    repository = MemberRepository()
    member = repository.get_by_id(member_id)
    
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    
    bookings = BookingModel.query.filter_by(
        member_id=member_id,
        is_active=True
    ).all()
    
    result = []
    for booking in bookings:
        result.append({
            'booking_reference': booking.booking_reference,
            'inventory_item_id': booking.inventory_item_id,
            'booking_date': booking.booking_date.isoformat()
        })
    
    return jsonify(result), 200