pipeline {
    agent any

    stages {
        stage('Run Tests') {
            steps {
                // Install pytest globally on the Jenkins node (no virtualenv)
                sh 'pip install --user pytest'

                // Run the tests and save results in the 'test_reports' directory
                sh '/var/lib/jenkins/.local/bin/pytest test_math.py --maxfail=1 --disable-warnings -q --junitxml=test_reports/results.xml'
            }
        }

        stage('Archive Test Results') {
            steps {
                // Create the test reports directory (if needed)
                sh 'mkdir -p test_reports'

                // Archive the XML test results file
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
