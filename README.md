# 🛢️ Sistema de Gestión de Inventario Petrolera

Sistema web profesional para la gestión de inventario y documentación técnica de mantenimiento en centrales petroleras. Incluye control de roles (administrador/operario), sistema de reportes, y despliegue automatizado con Docker y Railway.

[![CI/CD](https://github.com/FelipeGar17/Sis.InventoryPetrolera/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/FelipeGar17/Sis.InventoryPetrolera/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Demo en Vivo

**🚀 Aplicación desplegada:** [https://sisinventorypetrolera-production.up.railway.app/](https://sisinventorypetrolera-production.up.railway.app/)

> ⚠️ **Nota**: Si usas **Brave Browser**, desactiva los bloqueadores de anuncios para que funcione correctamente.

## 📋 Características

### 🔐 Sistema de Autenticación
- ✅ Login con JWT (tokens de 24 horas)
- ✅ Roles: **ADMIN** (gestión completa) y **USER** (operario, solo lectura)
- ✅ Encriptación bcrypt para contraseñas
- ✅ Redirección automática según rol
- 🆕 **Protección contra fuerza bruta** - Bloqueo temporal tras 5 intentos fallidos
- 🆕 **Logging de seguridad** - Registro de todos los eventos de autenticación

### 📦 Gestión de Inventario
- ✅ **Administrador**: CRUD completo de artículos (código, nombre, tipo, cantidad, ubicación, stock mínimo)
- ✅ **Operario**: Vista de solo lectura del inventario con DataTables
- ✅ Filtros y búsqueda avanzada
- ✅ Exportación a CSV/Excel
- 🆕 **Validación mejorada** - Validaciones robustas en creación de artículos
- 🆕 **Nuevos campos** - acquisition_date, observations, tipo

### 📝 Sistema de Reportes
- ✅ **4 Tipos de Reportes**: Falla, Mantenimiento, Observación, Solicitud
- ✅ **4 Estados**: Pendiente, En Revisión, Resuelto, Cerrado
- ✅ Operarios crean reportes sobre equipos específicos
- ✅ Administradores gestionan y responden reportes
- ✅ Historial completo con timestamps
- 🆕 **Estadísticas en tiempo real** - Análisis de reportes y tasa de respuesta

### 👥 Gestión de Usuarios (Admin)
- ✅ Crear/editar/eliminar usuarios
- ✅ Asignación de roles
- ✅ Búsqueda y filtros
- ✅ Interfaz con DataTables
- 🆕 **Búsqueda avanzada** - Buscar por username, email o nombre completo
- 🆕 **Filtros por rol y estado** - Consultas complejas de usuarios

### 📊 Monitoreo del Sistema (NEW)
- 🆕 Health check básico (`/api/health/`)
- 🆕 Salud de base de datos con estadísticas (`/api/health/db`)
- 🆕 Monitoreo detallado con métricas (`/api/health/detailed`)
- 🆕 Actividad de últimas 24 horas
- 🆕 Estados del servicio (HEALTHY, DEGRADED, UNHEALTHY)

## 🚀 Stack Tecnológico

### Backend
- **Flask 3.0.0** - Framework web Python
- **SQLAlchemy 3.1.1** - ORM para MySQL
- **Flask-Bcrypt** - Encriptación de contraseñas
- **PyJWT** - Autenticación con tokens
- **Gunicorn 21.2.0** - Servidor WSGI de producción

### Frontend
- **HTML5/CSS3** con **Tailwind CSS 3.4**
- **JavaScript** vanilla + **jQuery 3.7.0**
- **DataTables 1.13.6** - Tablas interactivas
- **SweetAlert2** - Alertas modernas

### Base de Datos
- **MySQL 8.0** (local/Docker/Railway)
- Migraciones con scripts SQL
- Datos de prueba incluidos

### DevOps
- **Docker** + **Docker Compose** - Contenedores
- **GitHub Actions** - CI/CD automatizado
- **Railway.app** - Despliegue en la nube
- **Pytest** - Suite de pruebas

## 📂 Estructura del Proyecto

```
Sis.Inventary/
├── backend/
│   ├── config/
│   │   ├── config.py          # Configuración (SECRET_KEY, DB)
│   │   └── database.py        # Conexión SQLAlchemy
│   ├── models/
│   │   ├── user.py            # Modelo Usuario
│   │   ├── article.py         # Modelo Artículo
│   │   └── report.py          # Modelo Reporte
│   ├── routes/
│   │   ├── auth_routes.py     # Login/Registro + Brute-force protection
│   │   ├── users_routes.py    # CRUD Usuarios + Búsqueda avanzada
│   │   ├── article_routes.py  # CRUD Inventario + Validación mejorada
│   │   ├── report_routes.py   # CRUD Reportes + Estadísticas
│   │   ├── health_routes.py   # Health checks + Monitoreo
│   │   ├── admin_tools.py     # Herramientas administrativas
│   │   └── main_routes.py     # Rutas frontend
│   └── app.py                 # Aplicación Flask
├── frontend/
│   ├── templates/
│   │   ├── admin/
│   │   │   └── dashboard.html # Dashboard Admin
│   │   ├── operario/
│   │   │   └── dashboard.html # Dashboard Operario
│   │   ├── login.html         # Página de login
│   │   ├── diagnostico.html   # Herramientas debug
│   │   └── clear-session.html # Limpiar sesión
│   └── static/
│       ├── css/
│       │   ├── dashboard.css
│       │   ├── datatable.css
│       │   ├── global.css
│       │   ├── modal.css
│       │   └── styles.css
│       └── js/
│           ├── api.js         # Cliente API REST
│           ├── auth.js        # Utilidades autenticación
│           ├── dashboard-admin.js
│           ├── dashboard-operario.js
│           ├── reports-management.js
│           ├── users-management.js
│           └── utils.js
├── database/
│   ├── init.sql               # Inicialización completa
│   ├── schema.sql             # Schema con índices optimizados
│   ├── insert_data.sql        # Datos de prueba
│   ├── update_articles.sql    # Migraciones
│   └── users_schema.sql       # Schema de usuarios
├── tests/
│   ├── __init__.py
│   └── test_health.py         # Tests de salud del sistema
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline CI/CD automatizado
├── Dockerfile                 # Imagen Docker multi-stage
├── docker-compose.yml         # Orquestación con MySQL
├── .env.example               # Variables de entorno ejemplo
├── .env                       # Variables de entorno local
├── .dockerignore              # Archivos ignorados en Docker
├── .gitignore                 # Archivos ignorados en Git
├── runtime.txt                # Especificación Python 3.11
├── requirements.txt           # Dependencias Python
├── Procfile                   # Configuración Procfile
├── create_admin.py            # Script para crear admin
├── run.py                     # Punto de entrada
├── CHANGELOG.md               # Registro de cambios v1.0.0
├── DEPLOYMENT.md              # Guía de despliegue
├── DEVOPS_SETUP.md            # Documentación DevOps
└── README.md                  # Este archivo
```

## ⚙️ Instalación y Ejecución

### Opción 1: Desarrollo Local (XAMPP)

```bash
# 1. Clonar repositorio
git clone https://github.com/FelipeGar17/Sis.InventoryPetrolera.git
cd Sis.InventoryPetrolera

# 2. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos MySQL (XAMPP)
# - Iniciar Apache y MySQL en XAMPP
# - Importar database/init.sql en phpMyAdmin

# 5. Configurar variables de entorno (opcional)
# Crear archivo .env con:
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=development

# 6. Ejecutar aplicación
python run.py

# 7. Acceder a http://localhost:5000
```

**Usuarios de Prueba:**
- **Admin**: `admin` / `admin123`
- **Operario**: `operario1` / `operario123`

### Opción 2: Docker Local

```bash
# 1. Construir y ejecutar
docker-compose up --build

# 2. Acceder a http://localhost:5000

# 3. Detener contenedores
docker-compose down

# Incluye MySQL automático + datos de prueba
```

### Opción 3: Despliegue en Railway.app (Recomendado)

Ver guía completa en **[DEPLOYMENT.md](DEPLOYMENT.md)** - Sección "Opción 2: Deploy en Railway.app"

**Pasos rápidos:**
1. Crear cuenta en [Railway.app](https://railway.app) con GitHub
2. New Project → Deploy from GitHub repo
3. Add MySQL database (automático)
4. Configurar variables de entorno:
   - `SECRET_KEY`: tu-clave-secreta
   - `FLASK_ENV`: production
   - `DATABASE_URL`: (auto-generado por Railway)
5. Generate domain → Acceder a tu app en línea

**💰 Costo**: $5 USD/mes de crédito gratis (suficiente para proyectos pequeños)

## 🧪 Pruebas

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=backend --cov-report=html
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Clave secreta JWT | `dev-secret-key` |
| `FLASK_ENV` | Entorno (development/production) | `development` |
| `DATABASE_URL` | URL MySQL completa | Auto (Railway) |
| `DB_HOST` | Host de MySQL | `localhost` |
| `DB_USER` | Usuario MySQL | `root` |
| `DB_PASSWORD` | Contraseña MySQL | `` |
| `DB_NAME` | Nombre base de datos | `inventario_petrolera` |

### Base de Datos

**Schema:**
- `users` - Usuarios del sistema
- `articles` - Inventario de equipos
- `reports` - Reportes de mantenimiento

Ver `database/init.sql` para estructura completa.

## 🚢 CI/CD Pipeline

GitHub Actions ejecuta automáticamente al hacer push:

1. **Lint** - Validación con Black y Flake8
2. **Test** - Suite de pruebas con pytest
3. **Build** - Construcción de imagen Docker
4. **Deploy** - Despliegue a Railway.app
5. **Notify** - Notificación de resultado

Ver [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)

## 📖 Documentación Adicional

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa de despliegue (Docker, Railway, GitHub Actions)
- **[DEVOPS_SETUP.md](DEVOPS_SETUP.md)** - Resumen ejecutivo de infraestructura DevOps

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Felipe García** - [@FelipeGar17](https://github.com/FelipeGar17)

## 🙏 Agradecimientos

- Flask y comunidad Python
- Railway.app por el hosting gratuito
- Tailwind CSS por el diseño moderno
- DataTables por las tablas interactivas

---

⭐ **¡Si te gusta el proyecto, dale una estrella!** ⭐
