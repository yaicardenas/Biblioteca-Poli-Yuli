pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = 'pipeline'
    }
    
    stage('Liberar puerto MySQL') {
        steps {
            sh '''
                echo "🔍 Buscando contenedor que tenga mapeado el puerto 3306 o 3307..."

                # Busca contenedores que publiquen 3306 o 3307 en el host
                CONTAINERS=$(docker ps --filter "publish=3306" --filter "publish=3307" --format "{{.ID}}")

                if [ -n "$CONTAINERS" ]; then
                    echo "⚠️  Encontrado(s) contenedor(es) usando 3306/3307:"
                    docker ps --filter "id=$CONTAINERS" --format "  -> {{.ID}} {{.Names}} ({{.Ports}})"

                    echo "🛑 Deteniendo y eliminando contenedor(es)..."
                    docker rm -f $CONTAINERS
                    echo "✅ Puerto liberado."
                else
                    echo "✅ Ningún contenedor usa 3306 ni 3307."
                fi
            '''
        }
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
                    docker-compose down -v
                '''
            }
        }

        stage('Desplegar') {
            steps {
                sh '''
                    echo "🚀 Desplegando contenedores..."
                    docker-compose up -d --build
                '''
            }
        }
    }
}
