pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Install pytest globally on the Jenkins node (no virtualenv)
                sh 'pip install --user pytest'

                // Update PATH to include the directory where pytest is installed
                sh 'export PATH=$PATH:/var/lib/jenkins/.local/bin'

                // Run the tests
                sh 'pytest test_math.py --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Zip Test Results') {
            steps {
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
