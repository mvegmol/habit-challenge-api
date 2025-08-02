# 🏃‍♂️ Habit Challenge API - Actividades Físicas

API REST para gestión de hábitos con enfoque en actividades físicas (correr, caminar, pasos) e integración automática de datos del clima.

## ✨ Características Principales

- 🏃‍♂️ **Actividades Físicas**: Correr, caminar y contador de pasos
- 🌤️ **Integración del Clima**: Datos automáticos del clima para actividades outdoor
- 📊 **Resúmenes Inteligentes**: Estadísticas de progreso por tipo de actividad
- 🔐 **Autenticación JWT**: Sistema seguro de usuarios
- 📱 **API RESTful**: Fácil integración con aplicaciones frontend/móviles

## 🚀 Inicio Rápido

### 1. Configuración del Entorno

```bash
# Clonar repositorio
git clone https://github.com/mvegmol/habit-challenge-api.git
cd habit-challenge-api

# Crear entorno virtual
python -m venv .venv
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r api/requirements.txt
```

### 2. Configuración de Variables de Entorno

```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus configuraciones:
# - DATABASE_URL (PostgreSQL)
# - OPENWEATHER_API_KEY (gratuita en openweathermap.org)
```

### 3. Base de Datos

```bash
# Migrar estructura de base de datos
python migrate_database.py

# O si usas Alembic:
alembic upgrade head
```

### 4. Ejecutar la API

```bash
cd api
uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000

⚠️ **Nota Importante**: El sistema de autenticación usa **email como username** para el login.

## 📚 Documentación

### APIs Principales

- **🏃‍♂️ Actividades Físicas**: Ver [API_PHYSICAL_ACTIVITIES.md](API_PHYSICAL_ACTIVITIES.md)
- **🔐 Autenticación**: Ver [AUTH_GUIDE.md](AUTH_GUIDE.md)
- **📖 Swagger UI**: http://localhost:8000/docs

### Ejemplos de Uso

#### Registrar Sesión de Running:
```json
POST /progress/
{
  "habit_id": 1,
  "date": "2025-08-02",
  "distance_km": 5.2,
  "duration_minutes": 32,
  "city": "Madrid"
}
```

#### Obtener Resumen Semanal:
```bash
GET /progress/summary/?days=7&activity_type=correr
```

**Respuesta:**
```json
{
  "activity_type": "correr",
  "days": 7,
  "total_distance_km": 23.4,
  "total_duration_minutes": 145,
  "average_pace": 6.2
}
```

## 🧪 Pruebas

### Colección de Postman 📮
Incluye una colección completa para probar todas las funcionalidades:

```bash
# Importar en Postman:
Habit_Challenge_API_Collection.postman_collection.json
```

**Características de la colección:**
- ✅ **80+ requests** con tests automáticos
- ✅ **Variables automáticas** (tokens, IDs)
- ✅ **Flujo completo** de autenticación a estadísticas
- ✅ **Casos de error** y validaciones
- ✅ **Documentación integrada**

Ver guía completa: [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)

### Scripts de Prueba
```bash
# Ejecutar suite de pruebas completa
python test_physical_activities.py

# Pruebas unitarias
pytest
```

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI + Python 3.13
- **Base de Datos**: PostgreSQL + SQLAlchemy
- **Autenticación**: JWT + OAuth2
- **Clima**: OpenWeatherMap API
- **Validación**: Pydantic
- **Tests**: pytest + httpx

## 📊 Tipos de Actividades Soportadas

| Tipo | Campos Requeridos | Datos del Clima | Cálculos Automáticos |
|------|------------------|-----------------|---------------------|
| 🏃‍♂️ Correr | distance_km, duration_minutes, city | ✅ | Pace (min/km) |
| 🚶‍♂️ Caminar | distance_km, duration_minutes, city | ✅ | Pace (min/km) |
| 👟 Pasos | steps | ❌ | Total de pasos |

## 🔧 Configuración Avanzada

### Variables de Entorno Completas:

```env
# Base de datos
DATABASE_URL=postgresql://user:pass@localhost:5432/habit

# JWT
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenWeatherMap (gratis)
OPENWEATHER_API_KEY=your-api-key

# App
DEBUG=true
APP_NAME=Habit Challenge API
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

- 📖 [Documentación completa](API_PHYSICAL_ACTIVITIES.md)
- 🐛 [Reportar bugs](https://github.com/mvegmol/habit-challenge-api/issues)
- 💬 [Discusiones](https://github.com/mvegmol/habit-challenge-api/discussions)