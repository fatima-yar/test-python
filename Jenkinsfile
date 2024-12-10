pipeline {
    agent any  

    stages {
        stage('Install and Run Tests') {
            steps {
                // Install pytest and run tests
                script {
                    // Install pytest
                    sh 'pip install pytest'
                    
                    // Run tests using pytest
                    sh 'pytest --maxfail=1 --disable-warnings -q'
                }
            }
        }

        stage('Download and Unzip Artifact') {
            steps {
                // Run the Python script to download and unzip the artifact
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
