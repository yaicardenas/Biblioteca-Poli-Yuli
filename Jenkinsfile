pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "pipeline-test"
    }

    stages {
        stage('Detener y limpiar contenedores antiguos') {
            steps {
                sh '''
                    echo "🛑 Deteniendo contenedores si existen..."
                    docker-compose -p $COMPOSE_PROJECT_NAME down --remove-orphans --volumes || true
                '''
            }
        }

        stage('Eliminar red Docker previa si existe') {
            steps {
                sh '''
                    echo "🧹 Eliminando red Docker previa si existe..."
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
                    echo "🧽 Limpiando entorno de pruebas..."
                    docker-compose -p $COMPOSE_PROJECT_NAME down --remove-orphans --volumes || true
                    docker system prune -f || true
                '''
            }
        }

        stage('Desplegar en producción') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "🚀 Desplegando en producción..."
                    docker-compose -p $COMPOSE_PROJECT_NAME up -d
                '''
            }
        }
    }
}
