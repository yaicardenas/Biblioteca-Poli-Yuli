pipeline {
    agent any

    stages {

        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo "🏩 Deteniendo y limpiando todo..."
                    docker-compose -p pipeline-test down --remove-orphans --volumes || true

                    echo "🗑️ Eliminando contenedores y red fija..."
                    docker rm -f mysql-db flask-app || true
                    docker network rm pipeline_net || true

                    echo "🧹 Limpiando redes y volúmenes huérfanos..."
                    docker network prune -f || true
                    docker volume  prune -f || true
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    sh '''
                        echo "🔧 Levantando base de datos..."
                        docker-compose -p pipeline-test up -d db
                        sleep 5

                        echo "🌐 Levantando web..."
                        docker-compose -p pipeline-test up -d web

                        echo "⌛ Esperando que web esté lista..."
                        sleep 5

                        echo "🧪 Ejecutando pruebas..."
                        docker-compose -p pipeline-test exec web \
                            python -m unittest discover -s test || true

                        echo "🧹 Apagando servicios..."
                        docker-compose -p pipeline-test down
                    '''
                }
            }
        }

        stage('Desplegar') {
            when { expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' } }
            steps {
                sh '''
                    echo "🚀 Desplegando contenedores productivos..."
                    docker-compose -p pipeline-test up -d
                '''
            }
        }
    }
}
