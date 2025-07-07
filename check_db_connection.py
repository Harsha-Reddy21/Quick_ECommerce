import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def check_connection():
    """Check connection to PostgreSQL database"""
    try:
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
        
        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a test query
        cur.execute("SELECT version();")
        
        # Get the result
        version = cur.fetchone()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        print("Successfully connected to PostgreSQL database!")
        print(f"PostgreSQL version: {version[0]}")
        return True
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return False

if __name__ == "__main__":
    check_connection() 