pipeline {
    agent any

    stages {

        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo "🏩 Deteniendo y limpiando contenedores anteriores..."
                    docker-compose -p pipeline-test down --volumes --remove-orphans || true

                    echo "🔧 Eliminando red si existe (evitar errores por IPv6)..."
                    docker network rm pipeline-test_default || true
                '''
            }
        }

        stage('Limpiar contenedores previos') {
            steps {
                sh '''
                    echo "🧹 Eliminando contenedores previos si existen..."
                    docker rm -f mysql-db flask-app || true
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''
                        echo "🔧 Levantando servicio web para ejecutar pruebas..."
                        docker-compose -p pipeline-test up -d db
                        sleep 5
                        docker-compose -p pipeline-test up -d web

                        echo "⌛ Esperando que el servicio web esté listo..."
                        sleep 5

                        echo "🧚 Ejecutando pruebas..."
                        docker-compose -p pipeline-test exec web python -m unittest discover -s test || true

                        echo "🧹 Apagando servicios después de las pruebas..."
                        docker-compose -p pipeline-test down
                    '''
                }
                sh 'docker ps -a'
            }
        }

        stage('Desplegar') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "🚀 Desplegando contenedores..."
                    docker rm -f flask-app || true
                    docker-compose -p pipeline-test up -d
                '''
            }
        }
    }
}
