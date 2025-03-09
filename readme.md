# Inventory Booking System

A Flask-based REST API for an inventory booking system that follows the repository pattern for clean architecture and demonstrates maintainable, scalable design principles.

## 📝 System Overview

This application allows members to book items from an inventory and cancel bookings, with the following features:

- CSV data import for members and inventory items
- Booking management with validation (max bookings per member)
- RESTful API endpoints
- Clean architecture with domain-driven design
- Detailed test coverage

## 🏗️ Architecture & Design Patterns

This project showcases several important software design principles:

- **Repository Pattern**: Separates data access logic from business logic
- **Domain-Driven Design**: Domain entities encapsulate business rules
- **Service Layer**: Orchestrates interactions between repositories
- **Clean Architecture**: Separation of concerns with clear dependencies
- **RESTful API**: Well-defined endpoints with proper HTTP methods and status codes

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ (make sure Python is installed on your system)
- PostgreSQL (or use the included Docker setup)

### Setup Options

You can run this application using either a local Python environment or Docker.

#### Option 1: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inventory-system.git
   cd inventory-system
   ```

2. **Create virtual environment**
   ```bash
   # If you're on macOS or Linux:
   python3 -m venv venv
   source venv/bin/activate

   # If you're on Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (see Environment Variables section below)

5. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Import sample data**
   ```bash
   # Make sure you have the CSV files in the data directory
   flask import-csv --members=data/members.csv --inventory=data/inventory.csv
   ```

7. **Run the application**
   ```bash
   flask run
   ```

8. **Access the API** at http://localhost:5000

#### Option 2: Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/inventory-system.git
   cd inventory-system
   ```

2. **Create .env file** (see Environment Variables section below)

3. **Build and start Docker containers**
   ```bash
   docker-compose up -d
   ```

4. **Import sample data**
   ```bash
   docker-compose exec web flask import-csv --members=data/members.csv --inventory=data/inventory.csv
   ```

5. **Access the API** at http://localhost:5000

## ⚙️ Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Flask configuration
SECRET_KEY=your_secret_key_here
FLASK_APP=run.py
FLASK_ENV=development

# Database configuration
# Use this for local development with Docker PostgreSQL:
DATABASE_URL=postgresql://postgres:password@db:5432/inventory

# Use this for local development with local PostgreSQL:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/inventory

```

## 🧪 Running Tests

```bash
# In local environment
pytest

# With Docker
docker-compose exec web pytest
```

## 📚 API Documentation

### Book an Item

**Endpoint**: `POST /api/book`

**Request Body**:
```json
{
  "member_id": 1,
  "item_title": "Bali"
}
```

**Successful Response** (201 Created):
```json
{
  "booking_reference": "AB12CD34",
  "member_name": "Sophie Davis",
  "item_title": "Bali",
  "booking_date": "2025-03-09T12:30:45"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Member has reached the maximum number of bookings (2)"
}
```

### Cancel a Booking

**Endpoint**: `POST /api/cancel`

**Request Body**:
```json
{
  "booking_reference": "AB12CD34"
}
```

**Successful Response** (200 OK):
```json
{
  "message": "Booking AB12CD34 cancelled successfully"
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Booking not found"
}
```

### Get All Inventory

**Endpoint**: `GET /api/inventory`

**Successful Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Bali",
    "description": "Suspendisse congue erat ac ex venenatis mattis...",
    "remaining_count": 5,
    "expiration_date": "2030-11-19"
  },
  {
    "id": 2,
    "title": "Madeira",
    "description": "Donec condimentum, risus non mollis sollicitudin...",
    "remaining_count": 4,
    "expiration_date": "2030-11-20"
  }
]
```

### Get Member Bookings

**Endpoint**: `GET /api/members/{member_id}/bookings`

**Successful Response** (200 OK):
```json
[
  {
    "booking_reference": "AB12CD34",
    "inventory_item_id": 1,
    "booking_date": "2025-03-09T12:30:45"
  }
]
```

**Error Response** (404 Not Found):
```json
{
  "error": "Member not found"
}
```

## 📝 Testing the API with cURL

Here are some cURL commands to test the API:

```bash
# Get all inventory items
curl -X GET http://localhost:5000/api/inventory

# Book an item
curl -X POST http://localhost:5000/api/book \
  -H "Content-Type: application/json" \
  -d '{"member_id": 1, "item_title": "Bali"}'

# Cancel a booking (replace AB12CD34 with your actual booking reference)
curl -X POST http://localhost:5000/api/cancel \
  -H "Content-Type: application/json" \
  -d '{"booking_reference": "AB12CD34"}'

# Get a member's bookings
curl -X GET http://localhost:5000/api/members/1/bookings
```

## 🗂️ Project Structure

```
inventory_system/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── config.py                # Configuration settings
│   ├── domain/                  # Domain models
│   │   ├── member.py            # Member domain entity
│   │   ├── inventory_item.py    # Inventory item domain entity
│   │   └── booking.py           # Booking domain entity
│   ├── repositories/            # Data access layer
│   │   ├── member_repository.py
│   │   ├── inventory_repository.py
│   │   └── booking_repository.py
│   ├── services/                # Business logic layer 
│   │   └── booking_service.py
│   ├── api/                     # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models/                  # SQLAlchemy models
│   │   ├── member.py
│   │   ├── inventory_item.py
│   │   └── booking.py
│   └── commands/                # CLI commands
│       ├── __init__.py
│       └── import_csv.py
├── migrations/                  # Database migrations
├── tests/                       # Unit tests
├── data/                        # CSV data files
├── .env                         # Environment variables
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── requirements.txt             # Python dependencies
└── run.py                       # Application entry point
```

## ⚠️ Design Considerations & Trade-offs

- **Repository Pattern**: Adds a layer of abstraction that helps with testing and future changes to the data storage mechanism, though it requires more code initially.
  
- **Domain Models**: Separating domain logic from database models allows for cleaner business rules but requires manual mapping between layers.

- **PostgreSQL**: Chosen for ACID compliance and relational features that fit this domain model well, though it requires more setup than SQLite.

## 🚀 Future Enhancements

- Add authentication and authorization
- Implement event-driven architecture for notifications
- Add reporting capabilities
