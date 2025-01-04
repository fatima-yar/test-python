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


        stage('Finish') {
            steps {
                echo "Successfully inserted values into test_c and test_python tables."
            }
        }
    }
}
