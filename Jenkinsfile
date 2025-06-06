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
                    sleep 5

                    echo "🧪 Ejecutando pruebas unitarias dentro del contenedor web..."
                    docker-compose -p pipeline-test exec web python -m unittest discover -s test || true

                    echo "🧹 Apagando servicio web después de las pruebas..."
                    docker-compose -p pipeline-test down
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
                    echo "🔧 Levantando entorno para pruebas (solo web y db)..."
                    docker-compose -p pipeline-test up -d --build web db
                '''
            }
        }
    }
}
