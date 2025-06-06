pipeline {
    agent any

    stages {
        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo "\uD83C\uDFE9 Deteniendo y limpiando contenedores anteriores..."
                    docker-compose -p pipeline-test down --volumes --remove-orphans || true
                '''
            }
        }

        stage('Limpiar contenedores previos') {
            steps {
                sh '''
                    echo "\uD83E\uDE9A Eliminando contenedores previos si existen..."
                    docker rm -f mysql-db jenkins-server flask-app || true
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    echo "\uD83D\uDD27 Levantando servicio web para ejecutar pruebas..."
                    docker-compose -p pipeline-test up -d db
                    docker-compose -p pipeline-test up -d web || true

                    echo "\u231B Esperando que el servicio web esté listo..."
                    sleep 5

                    echo "\uD83E\uDEF9 Ejecutando pruebas..."
                    docker-compose -p pipeline-test exec web python -m unittest discover -s test || true

                    echo "\uD83E\uDE9A Apagando servicios después de las pruebas..."
                    docker-compose -p pipeline-test down
                '''
            }
        }

        stage('Desplegar') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh '''
                    echo "\uD83D\uDE80 Desplegando contenedores..."
                    sleep 2
                    docker rm -f flask-app || true
                    sleep 2
                    docker-compose -p pipeline-test up -d || true
                '''
            }
        }
    }
}
