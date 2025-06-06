FROM jenkins/jenkins:lts

USER root

# Instala Docker y docker-compose desde los paquetes de Debian
RUN apt-get update && \
    apt-get install -y docker.io docker-compose && \
    usermod -aG docker jenkins

USER jenkins
