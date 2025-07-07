import psycopg2
from dotenv import load_dotenv
import os
import getpass

# Load environment variables
load_dotenv()

def get_postgres_credentials():
    """Get PostgreSQL credentials from user"""
    print("Enter PostgreSQL credentials:")
    host = input("Host (default: localhost): ") or "localhost"
    port = input("Port (default: 5432): ") or "5432"
    user = input("Username (default: postgres): ") or "postgres"
    password = getpass.getpass("Password: ")
    
    return host, port, user, password

def list_databases(host, port, user, password):
    """List all PostgreSQL databases"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=host,
            port=port,
            database="postgres",
            user=user,
            password=password
        )
        conn.autocommit = True
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute query to list all databases
        cur.execute("SELECT datname FROM pg_database;")
        
        # Get all databases
        databases = [row[0] for row in cur.fetchall()]
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
        print("\nAvailable PostgreSQL databases:")
        for db in databases:
            print(f"- {db}")
        
        return databases
    except Exception as e:
        print(f"\nError connecting to PostgreSQL: {e}")
        return []

def check_database(host, port, user, password, database_name):
    """Check if specific database exists and list its tables"""
    databases = list_databases(host, port, user, password)
    
    if database_name in databases:
        print(f"\n{database_name} database exists!")
        
        try:
            # Connect to the database
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database_name,
                user=user,
                password=password
            )
            
            # Create a cursor
            cur = conn.cursor()
            
            # List all tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            
            tables = [row[0] for row in cur.fetchall()]
            
            print(f"\nTables in {database_name} database:")
            if tables:
                for table in tables:
                    print(f"- {table}")
                    
                    # Get row count for each table
                    cur.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cur.fetchone()[0]
                    print(f"  Rows: {count}")
                    
                    # If table has rows, show sample data
                    if count > 0:
                        cur.execute(f"SELECT * FROM {table} LIMIT 3;")
                        columns = [desc[0] for desc in cur.description]
                        print(f"  Sample data (columns: {', '.join(columns)})")
                        for row in cur.fetchall():
                            print(f"    {row}")
            else:
                print("No tables found")
            
            # Close cursor and connection
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"Error connecting to {database_name} database: {e}")
    else:
        print(f"\n{database_name} database does not exist!")
        print("You need to create it using:")
        print(f"1. psql -U {user} -h {host} -p {port}")
        print(f"2. CREATE DATABASE {database_name};")
        print("3. \\q")
        print("\nOr update your .env file and run: python create_tables.py")

def main():
    """Main function"""
    print("PostgreSQL Database Checker")
    print("==========================")
    
    # Get PostgreSQL credentials
    host, port, user, password = get_postgres_credentials()
    
    # Get database name to check
    database_name = input("\nEnter database name to check (default: quickcommerce): ") or "quickcommerce"
    
    # Check database
    check_database(host, port, user, password, database_name)

if __name__ == "__main__":
    main() 