pipeline{
    agent any

    environment {
        PATH = "/usr/local/bin:$PATH"
    }

    stages {
      stage('Print Docker Compose Path') {
            steps {
                script {
                    // Run a command to find the path to docker-compose
                    def dockerComposePath = sh(script: 'which docker-compose', returnStdout: true).trim()
                    // Print the path to the console
                    echo "Docker Compose Path: ${dockerComposePath}"
                }
            }
        }
        stage('Build'){
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