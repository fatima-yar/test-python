pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                script {
                    // Install dependencies, e.g., pytest, if not already installed
                    sh 'pip install pytest'
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    // Run pytest to execute the test
                    sh 'pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }
    }

    post {
        always {
            // Clean up or perform any actions after the tests, e.g., notify on failure
            echo 'Pipeline completed.'
        }
    }
}
