pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        COMPOSE_PROJECT_NAME = 'pipeline-test'
    }

    stages {
        stage('Preparar entorno limpio') {
            steps {
                sh '''
                echo "🧯 Deteniendo contenedores anteriores..."
                docker stop web mysql-db || true

                echo "🗑 Eliminando contenedores anteriores con volúmenes..."
                docker rm -v web mysql-db || true

                echo "🔧 Eliminando redes antiguas específicas..."
                docker network rm pipeline_net || true
                docker network rm ${COMPOSE_PROJECT_NAME}_default || true

                echo "🧹 Limpiando volúmenes huérfanos..."
                docker volume prune -f || true
                docker volume rm ${COMPOSE_PROJECT_NAME}_mysql-data || true

                echo "🔄 Prune de redes no usadas..."
                docker network prune -f || true
                '''
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                echo "🔧 Construyendo servicios..."
                docker-compose -p ${COMPOSE_PROJECT_NAME} build --no-cache
                docker-compose -p ${COMPOSE_PROJECT_NAME} up -d db web

                echo "⏳ Esperando a que la base de datos esté disponible..."
                until docker exec mysql-db mysqladmin ping -h "127.0.0.1" --silent; do
                    echo "Esperando DB..."
                    sleep 5
                done

                echo "📄 Copiando script de inicialización a MySQL..."
                docker cp init.sql mysql-db:/init.sql
                if [ $? -ne 0 ]; then
                    echo "❌ Error al copiar init.sql"
                    exit 1
                fi

                echo "🛠 Ejecutando script de inicialización..."
                if ! docker exec mysql-db bash -c 'mysql -uroot -proot biblioteca < /init.sql'; then
                    echo "❌ Error al cargar init.sql"
                    exit 1
                fi

                echo "✅ Verificando que el servicio web esté arriba..."
                if ! docker-compose -p ${COMPOSE_PROJECT_NAME} ps web | grep 'Up'; then
                    echo "❌ Web no arrancó"
                    docker-compose -p ${COMPOSE_PROJECT_NAME} logs web
                    exit 1
                fi

                echo "🚦 Ejecutando pruebas unitarias..."
                docker exec -w /app -i web python -m unittest discover -s test -v > resultados_test.log 2>&1
                status=$?

                if [ $status -ne 0 ]; then
                    echo "❌ Pruebas fallaron:"
                    tail -n 50 resultados_test.log
                else
                    echo "✅ Pruebas OK"
                fi

                exit $status
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'resultados_test.log', onlyIfSuccessful: false
                }
            }
        }

        stage('Limpiar entorno Docker') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sh '''
                echo "🧹 Deteniendo entorno de pruebas..."
                docker-compose -p ${COMPOSE_PROJECT_NAME} down || true

                echo "🧼 Limpiando recursos no utilizados..."
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
                docker-compose -p prod up -d --build db web
                '''
            }
        }
    }
}
