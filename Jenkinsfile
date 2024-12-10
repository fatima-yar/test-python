pipeline {
    agent any  

    stages {
        stage('Install and Run Tests') {
            steps {
                script {
                    // Install pytest
                    sh 'pip install pytest'

                    // Add the directory where pytest is installed to PATH (if needed)
                    sh 'export PATH=$PATH:/var/lib/jenkins/.local/bin'

                    // Run the specific test file (test_math.py)
                    sh 'pytest test_math.py --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Download and Unzip Artifact') {
            steps {
                script {
                    // Run the Python script to download and unzip the artifact
                    sh 'python3 path/to/your/script.py'
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '**/target/*.zip', allowEmptyArchive: true
        }
    }
}
