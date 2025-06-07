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

                    echo 🔧 Eliminando redes antiguas específicas...
                    docker network rm pipeline_net || true
                    docker network rm pipeline-test_default || true
                    docker network rm pipeline-test_pipeline_net || true

                    echo 🔄 Prune de redes no usadas...
                    docker network prune -f || true
                '''
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                    echo "🔧 Levantando servicio de base de datos..."
                    docker-compose -p pipeline-test up -d db

                    echo "⌛ Esperando que la base de datos esté lista..."
                    # Espera simple, idealmente reemplazar por check real
                    sleep 15

                    echo "🔧 Levantando servicio web..."
                    docker-compose -p pipeline-test up -d web

                    echo "🧪 Ejecutando pruebas unitarias..."
                    docker-compose exec -T web python -m unittest discover -s test -v > resultados_test.log 2>&1
                    status=$?

                    echo "📄 Resultados de pruebas:"
                    cat resultados_test.log

                    exit $status
                '''
            }
        }

        stage('Limpiar entorno Docker') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sh '''
                    echo 🧹 Deteniendo entorno de pruebas (redundante, por si acaso)...
                    docker-compose -p pipeline-test down || true

                    echo 🗑 Limpiando recursos no utilizados...
                    docker system prune -f || true
                '''
            }
        }

        stage('Desplegar en producción') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sh '''
                    echo "🚀 Desplegando en producción..."
                    docker-compose -p pipeline-test up -d --build db web
                '''
            }
        }
    }
}
