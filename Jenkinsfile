pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Checkout your code from the repository
                checkout scm
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    // Set the path to your Docker Compose file
                    def dockerComposeFile = "docker-compose.yaml"

                    // Build and start services defined in the Docker Compose file
                    sh "docker-compose -f ${dockerComposeFile} up --build -d"

                    // Additional steps or commands as needed for your deployment
                    // ...

                    // Stop and remove the containers when done
                    // sh "docker-compose -f ${dockerComposeFile} down"
                }
            }
        }
    }
}
