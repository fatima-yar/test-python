from database_functions import create_connection, insert_into_test_c_and_test_python_table
import psycopg2
import os
import datetime

def main():
    try:
        # Create the connection and cursor
        print("Attempting to connect to the database...")
        conn, cur = create_connection()
        print("Database connection successful.")

        # Example directory, PR number, and created_at values
        test_c_directory = "./output/test-c"
        print("Test C Directory Path:", os.path.abspath(test_c_directory))  # This will print the absolute path
        pr_number = "PR-2291"
        created_at = "2024-01-01"
        
        # Make sure the directory exists and is valid
        if not os.path.exists(test_c_directory):
            print(f"Error: The directory {test_c_directory} does not exist.")
            return

        # Insert data into the 'test_c' table
        print(f"Inserting data into the {test_c_directory} folder into the test_c table...")
        insert_into_test_c_and_test_python_table(test_c_directory, pr_number, created_at, cur, 'test_c')

        # Commit changes to the database
        conn.commit()

        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error during the database operation: {e}")
        raise  # Reraise the exception to terminate the program with an error status

    finally:
        # Clean up by closing cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
