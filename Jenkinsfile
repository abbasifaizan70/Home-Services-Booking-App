pipeline{
    agent any

    environment {
        PATH = "/usr/local/bin:$PATH"
    }

    stages {
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