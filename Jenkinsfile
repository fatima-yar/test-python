pipeline {
    agent any

    environment {
        DB_HOST = 'localhost'
        DB_PORT = '5432'
        DB_USER = 'postgres'
        DB_PASSWORD = 'postgres'
        DB_NAME = 'postgres'
        PR_NUMBER = 'PR-2291'  // Example PR number
        CREATED_AT = '2024-01-01'  // Example created_at value
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Database Connection and Tables') {
            steps {
                script {
                    echo "Connecting to database and creating tables..."
                    
                    // Command to run the Python script that calls the create_tables function
                    def command = "python3 ${WORKSPACE}/main.py"
                    
                    try {
                        // Run the Python script that will call the create_tables function
                        sh command
                    } catch (Exception e) {
                        echo "Error creating connection and tables: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Terminating pipeline due to error in database setup.")
                    }
                }
            }
        }
          stage('Insert Data into test_c') {
            steps {
                script {
                    // Path to the test_c directory where the files are located
                    def test_c_Directory = "../test-python/output/test_c"
                    echo 'Inserting data into test_c...'
                    
                    // Command to insert data into test_c table
                    def command = """python3 ${WORKSPACE}/database_functions.py insert_into_test_c_and_test_python_table ${test_c_Directory} ${env.PR_NUMBER} ${env.CREATED_AT} 'test_c'"""
                    
                    try {
                        // Run the Python script that will insert data into the test_c table
                        sh command
                    } catch (Exception e) {
                        echo "Error inserting data into test_c: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error("Terminating pipeline due to error in data insertion into test_c.")
                    }
                }
            }
        }

        stage('Finish') {
            steps {
                echo "Successfully inserted values into test_c and test_python tables."
            }
        }
    }
}
