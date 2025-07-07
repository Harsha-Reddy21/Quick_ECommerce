import sqlite3
import psycopg2
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

def sqlite_to_postgres():
    """Migrate data from SQLite to PostgreSQL"""
    try:
        # Check if SQLite database exists
        if not os.path.exists("quickcommerce.db"):
            print("SQLite database not found. Nothing to migrate.")
            return False
        
        # Connect to SQLite database
        sqlite_conn = sqlite3.connect("quickcommerce.db")
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get database URL from environment variables
        database_url = os.getenv("DATABASE_URL")
        
        # Parse the database URL to extract connection parameters
        # Format: postgresql://username:password@host:port/database
        db_parts = database_url.replace("postgresql://", "").split("@")
        user_pass = db_parts[0].split(":")
        host_db = db_parts[1].split("/")
        host_port = host_db[0].split(":")
        
        username = user_pass[0]
        password = user_pass[1]
        host = host_port[0]
        port = host_port[1] if len(host_port) > 1 else "5432"
        database = host_db[1]
        
        # Connect to PostgreSQL
        pg_conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        pg_cursor = pg_conn.cursor()
        
        # Get all tables from SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = sqlite_cursor.fetchall()
        
        # For each table, migrate data
        for table in tables:
            table_name = table['name']
            print(f"Migrating table: {table_name}")
            
            # Skip SQLite internal tables
            if table_name.startswith('sqlite_'):
                continue
            
            # Get all records from SQLite table
            sqlite_cursor.execute(f"SELECT * FROM {table_name}")
            records = sqlite_cursor.fetchall()
            
            if not records:
                print(f"No records found in table {table_name}")
                continue
            
            # Get column names
            column_names = [description[0] for description in sqlite_cursor.description]
            
            # For each record, insert into PostgreSQL
            for record in records:
                # Convert record to dictionary
                record_dict = dict(zip(column_names, record))
                
                # Build INSERT statement
                columns = ", ".join(column_names)
                placeholders = ", ".join(["%s"] * len(column_names))
                values = [record_dict[column] for column in column_names]
                
                # Execute INSERT statement
                try:
                    pg_cursor.execute(
                        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
                        values
                    )
                except Exception as e:
                    print(f"Error inserting record into {table_name}: {e}")
                    pg_conn.rollback()
                    continue
            
            # Commit changes for this table
            pg_conn.commit()
            print(f"Successfully migrated {len(records)} records from table {table_name}")
        
        # Close connections
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        print("Migration completed successfully!")
        return True
    
    except Exception as e:
        print(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    print("Starting migration from SQLite to PostgreSQL...")
    sqlite_to_postgres() 