pipeline {
    agent any
     environment {
        // Define the path where the test results will be stored
        TEST_REPORT_PATH = 'test_reports/results.xml'
        DATABASE_SCRIPT = 'insert_pr_data.py' // Python script for inserting data into the DB
        PR_NUMBER = '229' // Example PR number, replace with actual dynamic value
        DB_HOST = 'localhost'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'
        DB_NAME = 'postgres'
    }

    stages {
        stage('Run Tests') {
            steps {
                // Install pytest globally on the Jenkins node (no virtualenv)
                sh 'pip install --user pytest'

                // Run the tests and save results in the 'test_reports' directory
                sh '/var/lib/jenkins/.local/bin/pytest test_math.py --maxfail=1 --disable-warnings -q --junitxml=test_reports/results.xml'
            }
        }

        stage('Push Test Results to Database') {
            steps {
                // Run the Python script to insert test result data into the database
                script {
                    writeFile file: 'insert_pr_data.py', text: """
import os
import psycopg2
import cbor2

# Database connection parameters
DB_HOST = "${DB_HOST}"
DB_USER = "${DB_USER}"
DB_PASSWORD = "${DB_PASSWORD}"
DB_NAME = "${DB_NAME}"

# Define the PR number and test results file path
PR_NUMBER = "${PR_NUMBER}"
FOLDER_PATH = "test_reports"
TABLE_NAME = "test_report"

# Function to create database table if it doesn't exist
def create_tables(cursor):
    create_script = ''' 
    CREATE TABLE IF NOT EXISTS pr (
        id serial primary key,
        pr_number varchar,
        file_name varchar,
        file_content bytea)
    '''
    cursor.execute(create_script)

# Function to insert XML file content into the database
def insert_useless_data(folder_path, pr_number, table_name, cursor):
    txt_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.xml'))]
    file_name = txt_files[0]
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, 'r') as file:
        file_text = file.read()
        file_content = cbor2.dumps(file_text)  # Convert file text to CBOR

        insert_script = f'INSERT INTO {table_name} (pr_number, file_name, file_content) VALUES ( %s, %s, %s)'
        insert_values = (pr_number, file_name, file_content)
        cursor.execute(insert_script, insert_values)

# Connect to the database and execute the insert operations
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    if conn:
        cur = conn.cursor()

        # Drop existing tables if they exist
        cur.execute('DROP TABLE IF EXISTS pr, test_report')

        # Create necessary tables
        create_tables(cur)

        # Insert the test report data into the database
        insert_useless_data(FOLDER_PATH, PR_NUMBER, TABLE_NAME, cur)

        # Commit changes
        conn.commit()

        print("Successfully inserted values into all tables.")
except Exception as error:
    print(f"Error: {error}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
"""
                    // Execute the Python script to push data to the database
                    sh 'python3 insert_pr_data.py'
                }
            }
        }
    }

    post {
        success {
            // Archive the zip file as the test results
            archiveArtifacts artifacts: 'test_reports.zip', allowEmptyArchive: true
        }

        failure {
            echo 'The pipeline failed. Check the logs for errors.'
        }
    }
}

// def create_tables(cursor):
//     create_script = ''' 
//                 CREATE TABLE IF NOT EXISTS pr (
//                     id serial primary key,
//                     pr_number varchar,
//                     file_name varchar,
//                     file_content text)

//                     '''
// def insert_useless_data(folder_path, pr_number, table_name, cursor):
       
//      txt_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.xml'))]
//      file_name = txt_files[0]
//      file_path = os.path.join(folder_path, file_name)
//      with open(file_path, 'r') as file:
//         file_text = file.read()
//         file_content = cbor2.dumps(file_text)

//         insert_script = f'INSERT INTO {table_name} (pr_number, file_name, file_content) VALUES ( %s, %s, %s)'
//         insert_values = (pr_number,file_name, file_content)
//      cursor.execute(insert_script, insert_values)

// try:
//     conn=create_connection()
//     if conn is not None:

//         cur = conn.cursor()

//         cur.execute('DROP TABLE IF EXISTS pr, format_c, format_python, lint_c,simulator, target, test_c, test_python') #every time it drops the table and makes a new one


//         create_tables(cur)


//         insert_pr_data(cur)

//         #insert usless ones
//         # insert_useless_data('<path to xml file in the pipeline>', pr_number, 'test_report', cur)






//         conn.commit()

//         print("Successfully inserted values into all tables.")


// except Exception as error:
//     print(f"Error: {error}")
// finally:
//     if cur:
//         cur.close()
//     if conn:
//         conn.close()

