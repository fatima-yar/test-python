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
 stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Debug Workspace') {
            steps {
                script {
                    sh 'ls -al ${WORKSPACE}'  // To check the contents of the workspace
                }
            }
        }
        stage('Create Database Connection and Tables') {
            steps {
                script {
                    echo "Connecting to database and creating tables..."
                    def command = "python3 ${WORKSPACE}/database_functions.py create_tables"
                    try {
                        sh command
                    } catch (Exception e) {
                        echo "Error creating connection and tables: ${e.message}"
                    }
                }
            }
        }
        stage('Create Database Connection and Tables') {
            steps {
                script {
                    // Call Python script to create the connection and tables
                    echo 'Connecting to database and creating tables...'
                    def command = "python3 ${WORKSPACE}/database_functions.py create_tables"
                    def process = command.execute()
                    process.waitFor()
                    def output = process.in.text
                    def error = process.err.text

                    if (error) {
                        error("Error creating connection and tables: ${error}")
                    } else {
                        echo "Tables created successfully: ${output}"
                    }
                }
            }
        }

        stage('Insert Data into test_c') {
            steps {
                script {
                    // Define the directory for test_c
                    def test_c_Directory = "../test-python/output/test_c"
                    echo 'Inserting data into test_c...'
                    def command = """python3 database_functions.py insert_into_test_c_and_test_python_table ${test_c_Directory} ${env.PR_NUMBER} ${env.CREATED_AT} 'test_c'"""
                    def process = command.execute()
                    process.waitFor()
                    def output = process.in.text
                    def error = process.err.text

                    if (error) {
                        error("Error inserting data into test_c: ${error}")
                    } else {
                        echo "Data inserted successfully into test_c: ${output}"
                    }
                }
            }
        }

        stage('Insert Data into test_python') {
            steps {
                script {
                    // Define the directory for test_python
                    def test_python_Directory = "../test-python/output/test_python"
                    echo 'Inserting data into test_python...'
                    def command = """python3 database_functions.py insert_into_test_c_and_test_python_table ${test_python_Directory} ${env.PR_NUMBER} ${env.CREATED_AT} 'test_python'"""
                    def process = command.execute()
                    process.waitFor()
                    def output = process.in.text
                    def error = process.err.text

                    if (error) {
                        error("Error inserting data into test_python: ${error}")
                    } else {
                        echo "Data inserted successfully into test_python: ${output}"
                    }
                }
            }
        }

        stage('Finish') {
            steps {
                script {
                    echo "Successfully inserted values into all tables."
                }
            }
        }
    }
}
