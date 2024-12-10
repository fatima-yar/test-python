pipeline {
    agent any  

    stages {
        stage('Install and Run Tests') {
            steps {
                script {
                    // Install pytest
                    sh 'pip install --user pytest'  // Use --user to install in the user directory

                    // Add the directory where pytest is installed to PATH
                    sh 'export PATH=$PATH:/var/lib/jenkins/.local/bin'

                    // Check if pytest is accessible
                    sh 'echo $PATH'  // Print the PATH to debug
                    sh 'which pytest'  // Check if pytest is found

                    // Run tests using pytest
                    sh 'pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Download and Unzip Artifact') {
            steps {
                script {
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

