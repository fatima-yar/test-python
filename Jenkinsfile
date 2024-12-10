pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Install pytest globally on the Jenkins node (no virtualenv)
                sh 'pip install --user pytest'

                // Run the tests using the full path to pytest
                sh '/var/lib/jenkins/.local/bin/pytest test_math.py --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Zip Test Results') {
            steps {
                // Ensure zip is installed before using it
                sh 'apt-get update && apt-get install -y zip || yum install -y zip'

                // Create and zip the test results directory
                sh 'mkdir -p test_reports && zip -r test_reports.zip test_reports/'
            }
        }
    }

    post {
        success {
            // Archive the zipped test results
            archiveArtifacts artifacts: 'test_reports.zip', allowEmptyArchive: true
        }
    }
}
