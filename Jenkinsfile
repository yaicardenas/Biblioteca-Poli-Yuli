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

        stage('Build y levantar entorno para pruebas') {
            steps {
                sh '''
                    echo 🔧 Levantando entorno para pruebas...
                    docker-compose -p pipeline-test up -d --build
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    echo 🧪 Ejecutando pruebas...
                    # aquí va tu comando de pruebas, por ejemplo:
                    docker exec flask-app pytest || exit 1
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
