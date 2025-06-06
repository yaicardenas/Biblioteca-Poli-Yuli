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
                '''
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                    echo "🔧 Levantando sólo el servicio web para pruebas..."
                    docker-compose -p pipeline-test up -d db web

                    echo "⏳ Esperando a que la base de datos esté disponible..."
                    until docker-compose exec -T web bash -c "echo > /dev/tcp/mysql-db/3306" 2>/dev/null; do
                        echo "Esperando base de datos..."
                        sleep 2
                    done

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
