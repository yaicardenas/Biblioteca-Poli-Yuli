pipeline {
    agent any

    stages {
        stage('Liberar puerto MySQL') {
            steps {
                sh '''
                    echo "🔍 Buscando contenedor que tenga mapeado el puerto 3306 o 3307..."

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

        stage('Ejecutar pruebas') {
            steps {
                sh '''
                    echo "🔧 Levantando servicio web para ejecutar pruebas..."
                    docker-compose up -d db
                    docker-compose up -d web

                    echo "⌛ Esperando que el servicio web esté listo..."
                    sleep 5

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
                    docker-compose up -d --build
                '''
            }
        }
    }
}
