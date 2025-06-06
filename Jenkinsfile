pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'pipeline'
    }

    stages {
        stage('Limpiar entorno previo') {
            steps {
                sh '''
                    echo "🧹 Limpiando entorno previo..."
                    docker-compose down -v --remove-orphans || true
                    docker network prune -f || true
                    echo "✅ Entorno limpio."
                '''
            }
        }

        stage('Construir contenedores') {
            steps {
                sh '''
                    echo "🔧 Construyendo contenedores..."
                    docker-compose build
                '''
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    echo "🔧 Levantando servicio web para ejecutar pruebas..."
                    docker-compose up -d db  # Levanta solo la base de datos si es necesaria
                    docker-compose up -d web

                    echo "⌛ Esperando que el servicio web esté listo..."
                    sleep 5  # Ajusta según tu app

                    echo "🧪 Ejecutando pruebas..."
                    docker-compose exec web python -m unittest discover -s test

                    echo "🧹 Apagando servicios después de las pruebas..."
                    docker-compose down
                '''
            }
        }

        stage('Desplegar') {
            steps {
                sh '''
                    echo "🚀 Desplegando contenedores..."
                    docker-compose up -d
                '''
            }
        }
    }
}
