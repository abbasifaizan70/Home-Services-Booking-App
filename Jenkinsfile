pipeline{
    agent any

    environment {
        PATH = "/usr/local/bin:$PATH"
    }

    stages {
      stage('Print Docker Compose Path') {
        stage('Build'){
          steps {
                script {
                    // Set the path to your Docker Compose file
                    def dockerComposeFile = "postgres-docker-compose.yaml"

                    // Build and start services defined in the Docker Compose file
                    sh "docker-compose -f ${dockerComposeFile} up --build -d"

                    // Additional steps or commands as needed for your deployment
                    // ...

                    // Stop and remove the containers when done
                    // sh "docker-compose -f ${dockerComposeFile} down"
                }
            }
            steps {
                sh '''
                docker-compose -f postgres-docker-compose.yaml up --build
                '''
            }
        }
        // stage('Setup Gunicorn Setup'){
        //     steps {
        //         sh '''
        //         chmod +x gunicorn.sh
        //         ./gunicorn.sh
        //         '''
        //     }
        // }
        // stage('setup NGINX'){
        //     steps {
        //         sh '''
        //         chmod +x nginx.sh
        //         ./nginx.sh
        //         '''
        //     }
        // }
      }
    }
}