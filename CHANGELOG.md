# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [1.0.0] - 2025-11-28

### ✨ Features Agregadas

#### Articles (Artículos)
- [x] Validación mejorada para creación de artículos
- [x] Función `validate_article_data()` con validaciones exhaustivas
- [x] Validación de longitud mínima para código y nombre (3+ caracteres)
- [x] Validación de stocks no negativos
- [x] Mensajes de error específicos y descriptivos

#### Reports (Reportes)
- [x] Endpoint `/statistics` para análisis de reportes
- [x] Cálculo de distribución por estado
- [x] Cálculo de distribución por tipo
- [x] Métrica de tasa de respuesta (porcentaje de reportes resueltos)
- [x] Estadísticas accesibles solo para administradores

#### Authentication (Autenticación)
- [x] Protección contra ataques de fuerza bruta
- [x] Rastreo de intentos de login fallidos
- [x] Bloqueo temporal de cuenta después de 5 intentos fallidos
- [x] Período de bloqueo de 15 minutos
- [x] Logging comprehensivo de eventos de seguridad
- [x] Códigos HTTP 429 para rate limiting

#### Users (Usuarios)
- [x] Búsqueda avanzada de usuarios
- [x] Búsqueda por username, nombre completo y email
- [x] Filtros por rol y estado
- [x] Ordenamiento por fecha de creación (más reciente primero)
- [x] Respuesta con contador de resultados para paginación

#### Health Checks (Monitoreo)
- [x] Versión y timestamp en endpoint base
- [x] Estadísticas de base de datos en `/db`
- [x] Nuevo endpoint `/detailed` con salud comprehensiva
- [x] Métricas de actividad últimas 24 horas
- [x] Estados de servicio: HEALTHY, DEGRADED, UNHEALTHY
- [x] Código HTTP 503 para servicios degradados

### 🐛 Bugfixes
- Manejo mejorado de excepciones en todas las rutas
- Validación más robusta de parámetros de entrada

### 🚀 Performance
- [x] Índices optimizados en tabla articles
- [x] Índices en columnas: location, tipo, created_at
- [x] Mejora en velocidad de consultas de filtrado
- [x] Soporte para análisis y reportes más eficientes

### 🏗️ Database (Base de Datos)
- [x] Adición de columnas: `acquisition_date`, `observations`, `tipo`
- [x] Índices estratégicos para mejor rendimiento
- [x] Esquema mejorado para mejor categorización de equipos

### 📝 Documentation
- [x] CHANGELOG.md - Registro de cambios
- [x] Commits semánticos con convenciones (feat, fix, perf, docs)

## Tipos de Commits

- **feat**: Una nueva característica
- **fix**: Una corrección de errores
- **docs**: Cambios solo en documentación
- **perf**: Cambios que mejoran el desempeño
- **test**: Agregando o actualizando tests
- **chore**: Cambios que no afectan el código (deps, config, etc)

## Próximas Features Planeadas

- [ ] Exportación de reportes a PDF/Excel
- [ ] Dashboard con gráficos en tiempo real
- [ ] Notificaciones por email
- [ ] Sistema de auditoría completo
- [ ] API de integración con terceros
- [ ] Mobile app
- [ ] Análisis predictivo de inventario

## Contribuciones

Las contribuciones son bienvenidas. Para cambios grandes, por favor abre un issue primero para discutir qué quieres cambiar.

Asegúrate de:
1. Actualizar tests según sea necesario
2. Seguir el formato de commits semánticos
3. Actualizar la documentación

## Contacto

Para preguntas o sugerencias, contacta a: nnico@example.com
