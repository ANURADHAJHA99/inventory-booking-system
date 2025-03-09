#!/bin/bash

source venv/bin/activate
pip install psycopg2-binary python-dotenv >/dev/null

python - << EOF
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_URL')

print(f"Testing database URL: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
    conn.close()
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
EOF
