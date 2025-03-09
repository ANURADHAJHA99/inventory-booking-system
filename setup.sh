#!/bin/bash
# Improved Setup script for Inventory Booking System

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=====================================================${NC}"
echo -e "${BLUE}      Inventory Booking System - Setup Script        ${NC}"
echo -e "${BLUE}=====================================================${NC}"

# Check for Python 3
echo -e "\n${YELLOW}Checking for Python 3...${NC}"
PYTHON_CMD=$(command -v python3 || command -v python)
if ! $PYTHON_CMD --version 2>&1 | grep -q 'Python 3'; then
    echo -e "${RED}Python 3 is required. Please install Python 3.${NC}"
    exit 1
fi
echo -e "${GREEN}Python 3 found: $($PYTHON_CMD --version)${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
$PYTHON_CMD -m venv venv || { echo -e "${RED}Failed to create virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment created.${NC}"

# Activate virtual environment
source venv/bin/activate || source venv/Scripts/activate || { echo -e "${RED}Failed to activate virtual environment.${NC}"; exit 1; }
echo -e "${GREEN}Virtual environment activated.${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt || { echo -e "${RED}Dependency installation failed.${NC}"; exit 1; }
echo -e "${GREEN}Dependencies installed successfully.${NC}"

# Setup .env file properly
echo -e "\n${YELLOW}Checking .env file...${NC}"
if [ ! -f .env ]; then
    read -rp "Enter your Supabase database password: " DB_PASS
    ENCODED_PASS=$(python -c "import urllib.parse; print(urllib.parse.quote('''$DB_PASS'''))")
    cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 16)
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:$ENCODED_PASS@db.wxixszituuzjiuhjedua.supabase.co:5432/postgres
MAX_BOOKINGS=2
EOF
    echo -e "${GREEN}.env file created successfully.${NC}"
else
    echo -e "${GREEN}.env file already exists. Checking format...${NC}"
    if grep -q "postgresql://postgres:@" .env; then
        echo -e "${RED}Warning: DATABASE_URL in .env seems incorrectly formatted.${NC}"
        read -rp "Enter your correct Supabase database password: " DB_PASS
        ENCODED_PASS=$(python -c "import urllib.parse; print(urllib.parse.quote('''$DB_PASS'''))")
        sed -i.bak "s|postgresql://postgres:@.*@|postgresql://postgres:$ENCODED_PASS@|" .env
        echo -e "${GREEN}.env file corrected.${NC}"
    fi
fi

# Initialize database
echo -e "\n${YELLOW}Initializing database...${NC}"
flask db init && flask db migrate -m "Initial migration" && flask db upgrade
if [ $? -ne 0 ]; then
    echo -e "${RED}Database initialization or migration failed. Check credentials and connection.${NC}"
    exit 1
fi
echo -e "${GREEN}Database set up successfully.${NC}"

# Import CSV data
echo -e "\n${YELLOW}Checking for CSV data...${NC}"
if [ -f "data/members.csv" ] && [ -f "data/inventory.csv" ]; then
    flask import-csv --members=data/members.csv --inventory=data/inventory.csv || echo -e "${RED}CSV import failed.${NC}"
    echo -e "${GREEN}CSV data imported successfully.${NC}"
else
    echo -e "${YELLOW}CSV files not found. Import manually later.${NC}"
fi

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\n${BLUE}Run the app using:${NC} ${YELLOW}flask run${NC}"
echo -e "${BLUE}Deactivate virtual environment:${NC} ${YELLOW}deactivate${NC}"
