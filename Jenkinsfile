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
                    docker-compose -p pipeline-test up -d web

                    echo "⌛ Esperando que el contenedor web esté listo..."
                    for i in {1..10}; do
                        if docker ps | grep -q "pipeline-test_web"; then
                            echo "✅ Contenedor web está listo."
                            break
                        fi
                        echo "⏳ Esperando... ($i/10)"
                        sleep 2
                    done

                    echo "🧪 Ejecutando pruebas unitarias dentro del contenedor web..."
                    docker-compose -p pipeline-test run --rm web python -m unittest discover -s test
                    status=$?

                    echo "🧹 Apagando servicio web después de las pruebas..."
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
