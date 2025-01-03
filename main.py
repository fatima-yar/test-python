from database_functions import create_connection, create_tables

def main():
    conn = create_connection()  # Establish connection
    try:
        cur = conn.cursor()  # Create cursor
        create_tables(cur)  # Call the function to create tables
        conn.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()  # Close the connection

if __name__ == "__main__":
    main()
