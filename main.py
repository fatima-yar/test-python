# Import the create_connection function from the relevant module if needed
from database_functions import create_connection
from database_functions import insert_into_test_c_and_test_python_table  
def main():
    try:
        # Create the connection and cursor
        conn, cur = create_connection()

        # Example directory, PR number, and created_at values
        test_c_directory = "../test-python/output/test_c"
        pr_number = "PR-2291"
        created_at = "2024-01-01"

        # Insert data into the 'test_c' table
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

