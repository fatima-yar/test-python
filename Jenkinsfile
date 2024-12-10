pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Create virtual environment and install pytest
                sh 'python3 -m venv venv'
                
                // Install dependencies using --user to avoid permission issues
                sh '. venv/bin/activate && pip install --user pytest'

                // Run the tests
                sh '. venv/bin/activate && pytest test_math.py --maxfail=1 --disable-warnings -q'
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
