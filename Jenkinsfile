pipeline {
    agent any

    stages {
      stage('Install Docker Compose') {
            steps {
                script {
                    sh 'sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose'
                    sh 'sudo chmod +x /usr/local/bin/docker-compose'
                }
            }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    // Set the path to your Docker Compose file
                    // def dockerComposeFile = "docker-compose.yaml"

                    // Build and start services defined in the Docker Compose file
                    sh "docker-compose -f postgres-docker-compose.yaml up --build -d"

                    // Additional steps or commands as needed for your deployment
                    // ...

                    // Stop and remove the containers when done
                    // sh "docker-compose -f ${dockerComposeFile} down"
                }
            }
        }
    }
}
