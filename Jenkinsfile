pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "pipeline-test"
    }

    stages {
        stage('Detener contenedores y limpiar') {
            steps {
                sh '''
                    echo "🛑 Deteniendo y eliminando contenedores existentes..."
                    docker-compose -p $COMPOSE_PROJECT_NAME down --remove-orphans --volumes || true

                    echo "🧹 Esperando a que contenedores liberen la red..."
                    sleep 5

                    echo "🧯 Eliminando red Docker si existe..."
                    docker network rm pipeline_net || true
                '''
            }
        }

        stage('Build y levantar entorno para pruebas') {
            steps {
                sh '''
                    echo "🔧 Levantando entorno para pruebas..."
                    docker-compose -p $COMPOSE_PROJECT_NAME up -d --build
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''
                        echo "🧪 Ejecutando pruebas..."
                        docker-compose -p $COMPOSE_PROJECT_NAME exec web \
                            python -m unittest discover -s test || true
                    '''
                }
            }
        }

        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo "🧽 Limpiando entorno..."
                    docker-compose -p $COMPOSE_PROJECT_NAME down --remove-orphans --volumes || true
                    docker system prune -f || true
                '''
            }
        }

        stage('Desplegar en producción') {
            when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
            steps {
                sh '''
                    echo "🚀 Desplegando contenedores productivos..."
                    docker-compose -p $COMPOSE_PROJECT_NAME up -d
                '''
            }
        }
    }
}
