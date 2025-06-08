pipeline {
    agent any

    stages {
        stage('Preparar entorno limpio') {
            steps {
                sh '''#!/bin/bash
                    echo 🧯 Deteniendo contenedores anteriores...
                    docker stop web mysql-db || true

                    echo 🗑 Eliminando contenedores anteriores...
                    docker rm web mysql-db || true

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
                sh '''#!/bin/bash
                    docker-compose -p pipeline-test up -d db web

                    until docker exec mysql-db mysqladmin ping -h "127.0.0.1" --silent; do
                        echo "Esperando DB..."
                        sleep 5
                    done

                    if ! docker-compose -p pipeline-test ps web | grep 'Up'; then
                        echo "Web no arrancó"
                        docker-compose -p pipeline-test logs web
                        exit 1
                    fi

                    docker-compose exec -T web python -m unittest discover -s test -v > resultados_test.log 2>&1
                    status=$?

                    if [ $status -ne 0 ]; then
                        echo "Pruebas fallaron:"
                        cat resultados_test.log
                    else
                        echo "Pruebas OK"
                    fi

                    exit $status
                '''
            }
        }


        stage('Limpiar entorno Docker') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                sh '''#!/bin/bash
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
                sh '''#!/bin/bash
                    echo "🚀 Desplegando en producción..."
                    docker-compose -p pipeline-test up -d --build db web
                '''
            }
        }
    }
}
