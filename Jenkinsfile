pipeline {
    agent any
    environment {
        DOCKER_COMPOSE_PATH = '/var/jenkins_home/docker-compose'
        POSTGRES_COMPOSE_FILE = 'postgres-docker-compose.yaml'
    }
    stages {
        stage('Install Docker Compose') {
          steps {
              script {
                  sh 'curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /var/jenkins_home/docker-compose'
                  sh 'chmod +x /var/jenkins_home/docker-compose'
              }
          }
        }

        stage('Build and Deploy') {
            steps {
                script {
                    sh "$DOCKER_COMPOSE_PATH -f $POSTGRES_COMPOSE_FILE up --build -d"
                }
            }
        }
    }
}
