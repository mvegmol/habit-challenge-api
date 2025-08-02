# 📮 Guía de la Colección de Postman - Habit Challenge API

Esta guía te ayudará a utilizar la colección de Postman para probar completamente la API de actividades físicas.

## 🚀 Configuración Inicial

### 1. Importar la Colección
```bash
1. Abre Postman
2. Haz clic en "Import"
3. Selecciona el archivo: Postman/Habit_Challenge_API_Collection.postman_collection.json
4. La colección aparecerá en tu sidebar
```

### 2. Configurar Variables de Entorno
La colección incluye variables automáticas, pero puedes personalizarlas:

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `base_url` | `http://localhost:8000` | URL base de tu API |
| `auth_token` | *(automático)* | Token JWT (se configura automáticamente) |
| `current_date` | *(automático)* | Fecha actual en formato YYYY-MM-DD |

### 3. Configurar Variables Personalizadas (Opcional)
```javascript
// En un Environment de Postman, puedes configurar:
{
  "base_url": "https://tu-api-en-produccion.com",
  "test_email": "tu-email-de-prueba@example.com",
  "test_password": "tu-password-de-prueba"
}
```

## 📋 Estructura de la Colección

### 🔐 1. Autenticación
**3 requests** con configuración automática de tokens:

- **Registrar Usuario**: Crea un nuevo usuario de prueba
- **Iniciar Sesión**: Obtiene token JWT (se guarda automáticamente)
- **Obtener Perfil**: Verifica que la autenticación funciona

### 🏃‍♂️ 2. Gestión de Hábitos  
**5 requests** para operaciones CRUD completas:

- **Crear Hábito - Correr**: Hábito para actividades de running
- **Crear Hábito - Caminar**: Hábito para caminatas
- **Crear Hábito - Pasos**: Hábito para conteo de pasos
- **Listar Mis Hábitos**: Obtiene todos los hábitos del usuario
- **Obtener por ID**: Detalles de un hábito específico

### 📊 3. Seguimiento de Progreso
**5 requests** con validación automática:

- **Registrar Running**: Sesión de correr con datos del clima
- **Registrar Caminata**: Sesión de caminar
- **Registrar Pasos**: Conteo diario de pasos
- **Ver Mi Progreso**: Todos los registros del usuario
- **Progreso por Hábito**: Progreso específico de un hábito

### 📈 4. Estadísticas y Resúmenes
**3 requests** con diferentes períodos:

- **Resumen Semanal - Correr**: Últimos 7 días
- **Resumen Mensual - Caminar**: Últimos 30 días  
- **Resumen de Pasos**: Últimas 2 semanas

### ❌ 5. Casos de Error
**4 requests** para validar manejo de errores:

- **Campos Faltantes**: Validación de campos requeridos
- **Valores Negativos**: Validación de rangos
- **Tipo Inválido**: Validación de tipos de actividad
- **Sin Autenticación**: Verificación de seguridad

### 🧪 6. Tests de Integración
**1 request** que verifica el estado general y variables.

## 🎯 Flujo de Uso Recomendado

### Opción A: Ejecución Manual (Paso a Paso)
```
1. 🔐 Autenticación → Registrar Usuario
2. 🔐 Autenticación → Iniciar Sesión  
3. 🏃‍♂️ Gestión de Hábitos → Crear Hábito - Correr
4. 🏃‍♂️ Gestión de Hábitos → Crear Hábito - Caminar
5. 🏃‍♂️ Gestión de Hábitos → Crear Hábito - Pasos
6. 📊 Seguimiento → Registrar Running
7. 📊 Seguimiento → Registrar Caminata
8. 📊 Seguimiento → Registrar Pasos
9. 📈 Estadísticas → Resumen Semanal - Correr
10. ❌ Casos de Error → (Ejecutar para ver validaciones)
```

### Opción B: Collection Runner (Automático)
```
1. Clic derecho en "Habit Challenge API - Physical Activities"
2. Seleccionar "Run collection"  
3. Configurar:
   - Iterations: 1
   - Delay: 1000ms (para evitar rate limits)
   - Save responses: Activado
4. Hacer clic en "Run Habit Challenge API"
```

## 🔧 Características Avanzadas

### Variables Automáticas
La colección configura automáticamente:

```javascript
// Pre-request Script global
if (!pm.environment.get('base_url')) {
    pm.environment.set('base_url', 'http://localhost:8000');
}
pm.environment.set('current_date', new Date().toISOString().split('T')[0]);
```

### Tests Automáticos
Cada request incluye tests que verifican:

```javascript
// Ejemplo de test automático
pm.test('Usuario registrado exitosamente', function () {
    pm.response.to.have.status(200);
});

pm.test('Token guardado automáticamente', function () {
    const response = pm.response.json();
    pm.expect(response).to.have.property('access_token');
});

// Auto-guardado de variables
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set('auth_token', response.access_token);
}
```

### Validaciones Incluidas
- ✅ **Status codes** correctos para cada endpoint
- ✅ **Estructura de respuesta** válida
- ✅ **Campos requeridos** presentes  
- ✅ **Tipos de datos** correctos
- ✅ **Auto-configuración** de variables
- ✅ **Manejo de errores** apropiado

## 📊 Interpretando los Resultados

### Panel de Test Results
```
✅ Tests Passed: 45/45    # Todos los tests pasaron
⏱️ Avg Response Time: 124ms    # Tiempo promedio de respuesta
📊 Total Requests: 15    # Total de requests ejecutados
```

### Variables Configuradas Automáticamente
Después de ejecutar la autenticación, verás:

```
auth_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
user_id: "1" 
habit_running_id: "1"
habit_walking_id: "2"  
habit_steps_id: "3"
current_date: "2025-08-03"
```

### Respuestas de Ejemplo

**Registro de Running con Clima:**
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
  "habit_id": 1
}
```

**Resumen Estadístico:**
```json
{
  "activity_type": "correr",
  "days": 7,
  "total_distance_km": 23.4,
  "total_duration_minutes": 145,
  "average_pace": 6.2
}
```

## 🛠️ Troubleshooting

### Problema: Token Expirado
```
Error: 401 Unauthorized
Solución: Re-ejecutar "Iniciar Sesión" para obtener nuevo token
```

### Problema: Variables No Configuradas
```
Error: Variables como {{habit_running_id}} aparecen sin resolver
Solución: Ejecutar los requests de creación de hábitos primero
```

### Problema: API No Responde
```
Error: Connection refused
Solución: 
1. Verificar que la API esté ejecutándose en localhost:8000
2. Actualizar base_url si usas otro puerto/host
```

### Problema: Tests Fallan
```
Error: Tests failing
Solución:
1. Verificar estructura de la base de datos
2. Confirmar que OPENWEATHER_API_KEY está configurado
3. Revisar logs de la API para errores específicos
```

## 🎨 Personalización

### Cambiar Datos de Prueba
Edita los body de los requests para usar tus propios datos:

```json
// En "Registrar Usuario"
{
  "email": "tu-email@example.com",
  "password": "TuPassword123",
  "full_name": "Tu Nombre"
}

// En "Registrar Running"  
{
  "distance_km": 10.5,        // Tu distancia
  "duration_minutes": 60,     // Tu tiempo
  "city": "Tu Ciudad"         // Tu ubicación
}
```

### Agregar Nuevos Tests
```javascript
// En la pestaña "Tests" de cualquier request
pm.test('Mi test personalizado', function () {
    const response = pm.response.json();
    pm.expect(response.pace).to.be.below(8); // Pace menor a 8 min/km
});
```

### Configurar para Producción
```json
// En Environment de Postman
{
  "base_url": "https://api.tudominio.com",
  "openweather_key": "tu-api-key-real"
}
```

## 📈 Métricas y Monitoreo

### KPIs que Puedes Rastrear
- **Tiempo de respuesta** promedio por endpoint
- **Tasa de éxito** de los tests (debe ser 100%)
- **Cobertura de funcionalidades** (todos los endpoints probados)
- **Validación de datos** (campos requeridos, tipos, rangos)

### Reportes Automáticos
Postman puede generar reportes HTML después de ejecutar la colección:

```
1. Ejecutar Collection Runner
2. Clic en "Export Results" 
3. Seleccionar formato (HTML, JSON, etc.)
4. Compartir con tu equipo
```

## 🚀 Siguientes Pasos

1. **Ejecuta la colección completa** para familiarizarte
2. **Personaliza los datos** según tus necesidades
3. **Agrega casos de prueba** específicos para tu uso
4. **Integra en CI/CD** usando Newman (CLI de Postman)
5. **Comparte con tu equipo** para testing colaborativo

## 🆘 Soporte

Si encuentras problemas:

1. **Revisa los logs** de la API en la consola
2. **Verifica variables** en el Environment tab de Postman  
3. **Ejecuta requests individualmente** para aislar problemas
4. **Consulta la documentación** de la API en `/docs`

¡Disfruta probando la API! 🏃‍♂️💨
