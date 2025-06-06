# 📚 Biblioteca-Poli

Proyecto Flask + MySQL con integración continua usando Jenkins y Docker.

---

## 🧱 Estructura del Proyecto

Biblioteca-Poli/
├── app/ # Aplicación Flask
│ ├── static/ # Archivos estáticos (CSS, JS, etc.)
│ │ └── css/
│ │  ├── estilos.css
│ │  └── hola_mundo.py
│ ├── templates/ # Plantillas HTML
│ ├── app.py # Entrada principal
│ ├── main.py # Lógica general
│ ├── hola_mundo.py # Script auxiliar
│ ├── Dockerfile # Dockerfile para la app Flask
│ └── requirements.txt # Dependencias de Python
│
├── jenkins/ # Configuración personalizada (opcional)
│ └── Dockerfile # Dockerfile de Jenkins (si se personaliza)
│
├── mysql-init/ # Scripts de inicialización de MySQL
│ └── init.sql
│
├── test/ # Pruebas automatizadas
│ └── tests.py
├── docker-compose.yml # Compose principal (usa Jenkins)
├── docker-compose-inicial.yml # Versión inicial (solo app + db)
├── Jenkinsfile # Pipeline de CI/CD
├── .gitignore
└── README.md

---

## 🚀 Tecnologías

- **Flask** (backend web)
- **MySQL** (base de datos)
- **Docker + Docker Compose**
- **Jenkins** (CI/CD)
- **GitHub Webhooks**

---

## ⚙️ Instalación Local

### 1. Levantar entorno sin Jenkins (solo para pruebas iniciales):

docker-compose -f docker-compose-inicial.yml up --build


### 2. Levantar entorno completo con Jenkins:
docker-compose up --build
Jenkins quedará disponible en: http://localhost:8080

App Flask en: http://localhost:5000

### 🧪 Pruebas Automatizadas
El archivo test/tests.py contiene pruebas de validación para la app.

### 🔄 Integración Continua con Jenkins
📁 Jenkinsfile
Contiene las etapas del pipeline:

Detener y limpiar contenedores anteriores.

Levantar entorno con docker-compose.

Ejecutar pruebas automatizadas.

Detener el entorno.

### 👥 Equipo de Desarrollo
Integrantes:

Diana Lucía Hernández Bayona

Anny Raquel Nieves Cuadrado

Karen Nicol Ñustes Florez

Johan Esteban Rodríguez Duarte

Yuliana Aide Cárdenas Jaramillo







