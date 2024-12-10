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

        stage('Archive Test Results') {
            steps {
                // Create the test results directory
                sh 'mkdir -p test_reports'

                // Instead of tar, directly create the zip file from the test_reports directory
                sh 'zip -r test_reports.zip test_reports/'
            }
        }
    }

    post {
        success {
            // Archive the zip file as the test results
            archiveArtifacts artifacts: 'test_reports.zip', allowEmptyArchive: true
        }
    }
}
