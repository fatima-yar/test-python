import os
import psycopg2
from database_functions import create_connection, create_tables

def create_connection():
    # Fetch the environment variables
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_name = os.getenv('DB_NAME', 'postgres')
    
    # Connect to the database using the environment variables
    conn = psycopg2.connect(
        dbname=db_name, 
        user=db_user, 
        password=db_password, 
        host=db_host, 
        port=db_port
    )
    return conn

def main():
    conn = create_connection()  # Establish the connection
    try:
        cur = conn.cursor()  # Create the cursor
        create_tables(cur)  # Call the function to create tables
        conn.commit()  # Commit the changes to the database
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()  # Close the cursor
        if conn:
            conn.close()  # Close the connection

if __name__ == "__main__":
    main()
