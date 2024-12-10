pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Install pytest and run the tests
                sh 'pip3 install pytest'
                sh 'pytest test_math.py --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Zip Test Results') {
            steps {
                // Create a directory for reports (if necessary) and zip the results
                sh 'mkdir -p test_reports'
                sh 'zip -r test_reports.zip test_reports/'
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
