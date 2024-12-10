pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Create and activate virtual environment, install pytest, and run tests
                sh 'python3 -m venv venv && . venv/bin/activate && pip install pytest && pytest test_math.py --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Zip Test Results') {
            steps {
                // Create and zip test results directory
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
