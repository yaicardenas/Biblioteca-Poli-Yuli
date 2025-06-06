pipeline {
    agent any

    stages {
        stage('Preparar entorno limpio') {
            steps {
                sh '''
                    echo 🧯 Deteniendo contenedores anteriores...
                    docker stop flask-app mysql-db || true

                    echo 🗑 Eliminando contenedores anteriores...
                    docker rm flask-app mysql-db || true

                    echo 🔧 Eliminando red de pruebas si está vacía...
                    docker network rm pipeline_net || true
                    docker network rm pipeline-test_default || true

                '''
            }
        }
        
        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                    echo "🧼 Limpiando redes antiguas..."
                    docker network prune -f || true

                    echo "🔧 Levantando sólo el servicio web para pruebas..."
                    docker-compose -p pipeline-test up -d db
                    docker-compose -p pipeline-test up -d web

                    echo "🧪 Ejecutando pruebas unitarias..."
                    docker-compose exec -T web python -m unittest discover -s test -v > resultados_test.log 2>&1
                    status=$?

                    echo "📄 Resultados de pruebas:"
                    cat resultados_test.log

                    echo "🧹 Apagando entorno..."
                    docker-compose -p pipeline-test down

                    exit $status
                '''
            }
        }


        stage('Limpiar entorno Docker') {
            steps {
                sh '''
                    echo 🧹 Deteniendo entorno de pruebas...
                    docker-compose -p pipeline-test down || true
                '''
            }
        }

        stage('Desplegar en producción') {
            steps {
                sh '''
                    echo "🔧 Levantando entorno"
                    docker-compose -p pipeline-test up -d --build web db
                '''
            }
        }
    }
}
