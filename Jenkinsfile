pipeline {
    agent any

    stages {
        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo "🛉 Deteniendo y limpiando contenedores anteriores..."
                    docker-compose -p pipeline-test down --volumes --remove-orphans || true
                '''
            }
        }

        stage('Limpiar contenedores previos') {
            steps {
                sh '''
                    echo "🧹 Eliminando contenedor mysql-db si ya existe..."
                    docker rm -f mysql-db || true
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    echo "🔧 Levantando servicio web para ejecutar pruebas..."
                    docker-compose -p pipeline-test up -d db
                    docker-compose -p pipeline-test up -d web || true

                    echo "⌛ Esperando que el servicio web esté listo..."
                    sleep 5

                    echo "🧚 Ejecutando pruebas..."
                    docker-compose -p pipeline-test exec web python -m unittest discover -s test || true

                    echo "🧹 Apagando servicios después de las pruebas..."
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
                    echo "🚀 Desplegando contenedores..."
                    docker rm -f jenkins-server flask-app || true
                    docker-compose -p pipeline-test up -d
                '''
            }
        }
    }
}
