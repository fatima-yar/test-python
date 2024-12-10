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

                // Use tar to compress the test results instead of zip
                sh 'tar -czf test_reports.tar.gz test_reports/'

                // Convert the .tar.gz file to .zip
                sh 'tar -xzf test_reports.tar.gz -C extracted_folder'  // Extract the tar.gz file
                sh 'zip -r test_reports.zip extracted_folder/*'         // Compress into a zip
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
