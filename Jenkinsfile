pipeline{
    agent any

    enviroment{
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('build') {
            steps {
                script {
                    sh 'docker-compose build'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                   sh '''
                       docker rm -f app_web || true
                       docker rm -f db || true
                       docker rm -f ci_jenkins || true
                       docker-compose down || true
                       docker-compose up -d
                   '''
                }
            }
        }

    }
}