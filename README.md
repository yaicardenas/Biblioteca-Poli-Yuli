# 📚 Biblioteca-Poli

Proyecto Flask + MySQL con integración continua usando Jenkins y Docker.

---

## 🧱 Estructura del Proyecto
<pre> 
Biblioteca-Poli/
├── .github                      # Aplicación Flask
│   └──workflows/  
│       └── ci.yml              # Workflow de CI/CD para GitHub Actions
├── app/                        # Aplicación Flask
│   ├── static/                # Archivos estáticos (CSS, JS)
│   │   └── css/
│   │       └── estilos.css
│   ├── templates/             # Plantillas HTML
│   ├── app.py                 # Entrada principal
│   ├── main.py                # Lógica principal
│   ├── hola_mundo.py          # Script auxiliar
│   ├── Dockerfile             # Dockerfile para la app Flask
│   └── requirements.txt       # Dependencias
│
├── jenkins/
│   └── Dockerfile             # Dockerfile para Jenkins (si se personaliza)
│
├── mysql-init/
│   └── init.sql               # Script de inicialización de base de datos
│
├── test/
│   └── tests.py               # Pruebas automatizadas
│
├── docker-compose.yml         # Compose principal (usa Jenkins)
├── docker-compose-inicial.yml # Solo app + DB sin Jenkins
├── Jenkinsfile                # Pipeline CI/CD
├── .gitignore
└── README.md
</pre>

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







