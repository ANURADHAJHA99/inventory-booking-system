# Inventory Booking System

A Flask-based REST API for inventory management that implements clean architecture principles and showcases the use of design patterns for maintainable, scalable code.

## 📝 System Overview

This application manages an inventory booking system with the following capabilities:

- Members can book items from the inventory (with validation)
- Members can cancel their bookings
- CSV data import for bulk loading members and inventory
- RESTful API endpoints with proper status codes and error handling
- Maximum booking limit per member (defined in constants)
- Expiration date validation for inventory items

## 🏗️ Architecture & Design Patterns

This project demonstrates my understanding and implementation of several software engineering principles:

### Repository Pattern
I've implemented repositories to abstract data access, making it easier to:
- Mock database access for unit testing
- Swap out the underlying database technology if needed
- Keep business logic free of data access concerns

### Singleton Pattern
The application uses singletons for repositories and services to:
- Ensure a single instance exists throughout the application lifecycle
- Reduce memory usage and improve performance
- Provide a global access point without passing references

### Dependency Injection
Services are designed with dependency injection to:
- Decouple components for better testability
- Make dependencies explicit
- Enable flexibility in providing different implementations

### Domain-Driven Design
The domain layer contains rich models that:
- Encapsulate business rules and validation
- Represent the ubiquitous language of the domain
- Separate business logic from persistence concerns

### Service Layer Pattern
The service layer orchestrates interactions between repositories and contains transaction boundaries, ensuring:
- Business operations happen atomically
- Separation of concerns between API controllers and data access
- Reusability of business logic across different entry points

### Constants for Business Rules
Business rules like the maximum number of bookings per member are defined as constants in a dedicated file:
- Makes business rules explicit and centralized
- Avoids embedding rules in environment variables
- Provides clear documentation of business constraints

## 📋 Project Requirements

The application was designed to meet the following requirements:

- Upload CSV files (via command line) and write data to a database
- Book an item from inventory for a member
- Cancel a booking based on a booking reference
- Track booking history with timestamps
- Enforce a maximum number of bookings per member
- Validate inventory availability
- Provide a RESTful API for these operations

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
SECRET_KEY=use_a_strong_random_key_in_production
FLASK_APP=run.py
FLASK_ENV=development

# Database configuration - choose one of these options

# For Docker:
DATABASE_URL=postgresql://postgres:password@db:5432/inventory

# For local PostgreSQL:
# DATABASE_URL=postgresql://postgres:password@localhost:5432/inventory

# For simple SQLite setup:
# DATABASE_URL=sqlite:///app.db
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
│   ├── constants.py             # Business rule constants
│   ├── domain/                  # Domain models (business entities)
│   │   ├── member.py            # Member domain entity
│   │   ├── inventory_item.py    # Inventory item domain entity
│   │   └── booking.py           # Booking domain entity
│   ├── repositories/            # Data access layer
│   │   ├── member_repository.py # Member data operations
│   │   ├── inventory_repository.py # Inventory data operations
│   │   └── booking_repository.py # Booking data operations
│   ├── services/                # Business logic layer 
│   │   └── booking_service.py   # Booking business logic
│   ├── api/                     # API routes
│   │   ├── __init__.py          # API blueprint registration
│   │   └── routes.py            # API endpoints
│   ├── models/                  # SQLAlchemy models
│   │   ├── member.py            # Database model for members
│   │   ├── inventory_item.py    # Database model for inventory
│   │   └── booking.py           # Database model for bookings
│   └── commands/                # CLI commands
│       ├── __init__.py          # Command registration
│       └── import_csv.py        # CSV import command
├── migrations/                  # Database migrations
├── tests/                       # Unit tests
│   ├── test_models.py           # Tests for database models
│   ├── test_repositories.py     # Tests for repositories
│   ├── test_services.py         # Tests for business logic
│   └── test_api.py              # Tests for API endpoints
├── data/                        # CSV data files
│   ├── members.csv              # Sample member data
│   └── inventory.csv            # Sample inventory data
├── .env                         # Environment variables
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── .gitignore                   # Git ignore configuration
├── requirements.txt             # Python dependencies
└── run.py                       # Application entry point
```

## ⚠️ Design Considerations & Trade-offs

### Repository Pattern
- **Pros**: Abstracts data access, makes testing easier, provides a clean separation of concerns
- **Trade-offs**: Requires more code than direct database access, adds a layer of indirection

### Domain Models vs ORM Models
- **Pros**: Domain models can encapsulate business rules without being tied to a database schema
- **Trade-offs**: Requires mapping between domain and ORM models, which adds complexity

### Singleton Pattern for Services
- **Pros**: Ensures consistent state, reduces resource usage
- **Trade-offs**: Can make unit testing more complex if not implemented carefully

### Business Rules as Constants
- **Pros**: Centralizes business rules, makes them explicit in code, improves maintainability
- **Trade-offs**: Requires code changes and redeployment to modify business rules

### PostgreSQL Database
- **Pros**: ACID compliance, robust relational features, good for data integrity
- **Trade-offs**: Requires more setup than SQLite, more complex deployment

## 🚀 Future Enhancements

- **Authentication and Authorization**: Add JWT or OAuth2 for secure API access
- **Event-Driven Architecture**: Implement event emission for actions like bookings and cancellations
- **API Rate Limiting**: Add protection against API abuse
- **Advanced Reporting**: Add endpoints for generating statistics and reports
- **Frontend Application**: Develop a web interface for managing the inventory system
- **Caching Layer**: Implement Redis caching for frequently accessed data
- **API Documentation**: Add Swagger/OpenAPI documentation
- **Business Rules Configuration**: Move hard-coded business rules to a configuration system