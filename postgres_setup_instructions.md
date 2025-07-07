# PostgreSQL Setup Instructions

This document provides instructions for setting up the Quick ECommerce application with PostgreSQL instead of SQLite.

## Prerequisites

1. Install PostgreSQL on your system
   - Windows: Download and install from https://www.postgresql.org/download/windows/
   - macOS: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql postgresql-contrib`

2. Create a PostgreSQL database
   ```sql
   CREATE DATABASE quickcommerce;
   ```

## Configuration Steps

1. Update the `.env` file with your PostgreSQL connection details:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/quickcommerce
   ```
   Replace `username` and `password` with your PostgreSQL credentials.

2. Install the required Python packages:
   ```bash
   pip install psycopg2-binary
   ```

3. Check database connection:
   ```bash
   python check_db_connection.py
   ```

4. Initialize the database tables:
   ```bash
   python create_tables.py
   ```

5. (Optional) If you have existing data in SQLite that you want to migrate:
   ```bash
   python migrate_sqlite_to_postgres.py
   ```

## Changes Made to the Codebase

1. Updated `app/database/database.py` to use PostgreSQL instead of SQLite
   - Removed SQLite-specific connection arguments
   - Updated the database URL

2. Updated Pydantic schemas to use `from_attributes` instead of `orm_mode`
   - This change was made to comply with Pydantic v2 standards

3. Fixed the delivery.py router to use the correct Pydantic schema
   - Added missing `DeliveryEstimateResponse` schema

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Troubleshooting

1. If you encounter connection issues:
   - Verify PostgreSQL is running
   - Check your credentials in the `.env` file
   - Ensure the database exists

2. If you encounter schema errors:
   - Run `python create_tables.py` to recreate the tables

3. For permission issues:
   - Ensure your PostgreSQL user has the necessary permissions 