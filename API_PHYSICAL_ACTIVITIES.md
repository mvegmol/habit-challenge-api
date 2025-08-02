# 🏃‍♂️ API de Actividades Físicas - Documentación Completa

Esta documentación detalla todos los endpoints disponibles para el sistema de seguimiento de actividades físicas.

## 🎯 Tipos de Actividades Soportadas

### 1. Correr 🏃‍♂️
- **Campos requeridos**: `distance_km`, `duration_minutes`, `city`
- **Cálculos automáticos**: `pace` (min/km)
- **Integración**: Datos del clima automáticos

### 2. Caminar 🚶‍♂️  
- **Campos requeridos**: `distance_km`, `duration_minutes`, `city`
- **Cálculos automáticos**: `pace` (min/km)
- **Integración**: Datos del clima automáticos

### 3. Pasos 👟
- **Campos requeridos**: `steps`
- **Cálculos automáticos**: Total de pasos
- **Integración**: Sin datos del clima

## 🔐 Autenticación

Todos los endpoints requieren autenticación JWT. Incluye el header:
```
Authorization: Bearer tu_jwt_token_aqui
```

## 📋 Endpoints de Hábitos

### Crear Hábito
```http
POST /habits/
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Correr por las mañanas",
  "description": "Sesión de running matutina",
  "activity_type": "correr",
  "is_public": true
}
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Correr por las mañanas",
  "description": "Sesión de running matutina",
  "activity_type": "correr",
  "is_public": true,
  "owner_id": 1,
  "created_at": "2025-08-03T10:30:00"
}
```

### Obtener Mis Hábitos
```http
GET /habits/me
Authorization: Bearer {token}
```

### Obtener Hábito por ID
```http
GET /habits/{habit_id}
Authorization: Bearer {token}
```

### Actualizar Hábito
```http
PUT /habits/{habit_id}
Content-Type: application/json
Authorization: Bearer {token}

{
  "title": "Correr por las tardes",
  "activity_type": "correr"
}
```

### Eliminar Hábito
```http
DELETE /habits/{habit_id}
Authorization: Bearer {token}
```

## 📊 Endpoints de Progreso

### Registrar Progreso - Correr/Caminar
```http
POST /progress/
Content-Type: application/json
Authorization: Bearer {token}

{
  "habit_id": 1,
  "date": "2025-08-03",
  "distance_km": 5.2,
  "duration_minutes": 32,
  "city": "Madrid"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "date": "2025-08-03",
  "distance_km": 5.2,
  "duration_minutes": 32,
  "pace": 6.15,
  "city": "Madrid",
  "weather_temperature": 22.5,
  "weather_description": "cielo claro",
  "weather_humidity": 65,
  "wind_speed": 3.2,
  "user_id": 1,
  "habit_id": 1,
  "created_at": "2025-08-03T10:30:00"
}
```

### Registrar Progreso - Pasos
```http
POST /progress/
Content-Type: application/json
Authorization: Bearer {token}

{
  "habit_id": 3,
  "date": "2025-08-03",
  "steps": 10500
}
```

**Respuesta:**
```json
{
  "id": 2,
  "date": "2025-08-03",
  "steps": 10500,
  "user_id": 1,
  "habit_id": 3,
  "created_at": "2025-08-03T10:30:00"
}
```

### Obtener Mi Progreso
```http
GET /progress/me
Authorization: Bearer {token}
```

### Obtener Progreso por Hábito
```http
GET /progress/habit/{habit_id}
Authorization: Bearer {token}
```

## 📈 Resúmenes y Estadísticas

### Resumen de Actividades - Correr/Caminar
```http
GET /progress/summary/?days=7&activity_type=correr
Authorization: Bearer {token}
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

### Resumen de Actividades - Pasos
```http
GET /progress/summary/?days=30&activity_type=pasos
Authorization: Bearer {token}
```

**Respuesta:**
```json
{
  "activity_type": "pasos",
  "days": 30,
  "total_steps": 315000
}
```

### Parámetros de Consulta

| Parámetro | Tipo | Rango | Descripción |
|-----------|------|-------|-------------|
| `days` | integer | 1-365 | Número de días para el resumen |
| `activity_type` | string | "correr", "caminar", "pasos" | Tipo de actividad |

## 🌤️ Integración del Clima

### Configuración
Para activar la integración del clima, configura tu API key de OpenWeatherMap:

```env
OPENWEATHER_API_KEY=tu_api_key_aqui
```

Obtén una API key gratuita en: https://openweathermap.org/api

### Datos Incluidos
- **Temperatura**: En grados Celsius
- **Descripción**: Condiciones meteorológicas en español
- **Humedad**: Porcentaje de humedad
- **Velocidad del viento**: En metros por segundo

### Ejemplo de Datos del Clima
```json
{
  "weather_temperature": 22.5,
  "weather_description": "cielo claro",
  "weather_humidity": 65,
  "wind_speed": 3.2
}
```

## ❌ Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| 400 | Datos de entrada inválidos | Verifica los campos requeridos |
| 401 | No autenticado | Incluye el token JWT válido |
| 403 | Sin permisos | Solo puedes modificar tus propios datos |
| 404 | Recurso no encontrado | Verifica que el ID exista |
| 422 | Error de validación | Revisa el formato de los datos |

## 📝 Ejemplos de Validación

### Errores Comunes

**Actividad de correr sin campos requeridos:**
```json
{
  "detail": "Para actividades de correr/caminar se requieren: distance_km, duration_minutes y city"
}
```

**Valores negativos:**
```json
{
  "detail": [
    {
      "loc": ["distance_km"],
      "msg": "distance_km debe ser mayor que 0",
      "type": "value_error"
    }
  ]
}
```

**Tipo de actividad inválido:**
```json
{
  "detail": [
    {
      "loc": ["activity_type"],
      "msg": "activity_type debe ser \"correr\", \"caminar\" o \"pasos\"",
      "type": "value_error"
    }
  ]
}
```

## 🔍 Casos de Uso Comunes

### 1. Sesión de Running Completa
```bash
# 1. Crear hábito de correr
POST /habits/ {"title": "Running matutino", "activity_type": "correr"}

# 2. Registrar sesión
POST /progress/ {"habit_id": 1, "date": "2025-08-03", "distance_km": 5, "duration_minutes": 30, "city": "Madrid"}

# 3. Ver progreso semanal
GET /progress/summary/?days=7&activity_type=correr
```

### 2. Seguimiento de Pasos Diario
```bash
# 1. Crear hábito de pasos
POST /habits/ {"title": "Meta diaria de pasos", "activity_type": "pasos"}

# 2. Registrar pasos del día
POST /progress/ {"habit_id": 2, "date": "2025-08-03", "steps": 12000}

# 3. Ver total mensual
GET /progress/summary/?days=30&activity_type=pasos
```

### 3. Análisis de Rendimiento
```bash
# Ver todas mis actividades
GET /progress/me

# Comparar diferentes períodos
GET /progress/summary/?days=7&activity_type=correr   # Semana actual
GET /progress/summary/?days=30&activity_type=correr  # Mes completo
```

## 🚀 Tips para Desarrolladores

### 1. Optimización de Consultas
- Usa los parámetros `days` apropiados para evitar consultas innecesarias
- Los resúmenes están optimizados para rangos de hasta 365 días

### 2. Manejo de Errores del Clima
- La API funciona aunque el servicio del clima falle
- Los campos de clima serán `null` si no hay conectividad

### 3. Cálculos Automáticos
- El `pace` se calcula automáticamente: `duration_minutes / distance_km`
- No envíes este campo en las peticiones POST

### 4. Fechas
- Usa formato ISO 8601: `YYYY-MM-DD`
- Las fechas futuras están permitidas para planificación

## 📱 Integración Frontend

### JavaScript/TypeScript
```javascript
// Registrar progreso de correr
const registerRun = async (data) => {
  const response = await fetch('/progress/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      habit_id: 1,
      date: '2025-08-03',
      distance_km: 5.2,
      duration_minutes: 32,
      city: 'Madrid'
    })
  });
  return response.json();
};

// Obtener resumen semanal
const getWeeklySummary = async (activityType) => {
  const response = await fetch(`/progress/summary/?days=7&activity_type=${activityType}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

## 🧪 Testing

Para probar la API, puedes usar la colección de Postman incluida o curl:

```bash
# Obtener token de autenticación
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Usar el token para crear un hábito
curl -X POST "http://localhost:8000/habits/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "Running matutino", "activity_type": "correr"}'
```

¿Necesitas más información sobre algún endpoint específico? ¡Consulta la documentación interactiva en `/docs`!
