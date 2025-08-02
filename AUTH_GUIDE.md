# Habit Challenge API - Autenticación

## Endpoints de Autenticación

### 1. Registro de Usuario
```http
POST /auth/register
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "miPassword123",
    "full_name": "Juan Pérez"
}
```

**Respuesta:**
```json
{
    "id": 1,
    "email": "usuario@ejemplo.com",
    "full_name": "Juan Pérez",
    "created_at": "2025-08-02T10:30:00"
}
```

### 2. Inicio de Sesión
```http
POST /auth/login
Content-Type: application/json

{
    "email": "usuario@ejemplo.com",
    "password": "miPassword123"
}
```

**Respuesta:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### 3. Obtener información del usuario actual
```http
GET /auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Respuesta:**
```json
{
    "id": 1,
    "email": "usuario@ejemplo.com",
    "full_name": "Juan Pérez",
    "created_at": "2025-08-02T10:30:00"
}
```

### 4. Token OAuth2 (compatible con FastAPI docs)
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=usuario@ejemplo.com&password=miPassword123
```

## Endpoints de Usuarios

### 1. Obtener lista de usuarios (requiere autenticación)
```http
GET /users/
Authorization: Bearer token_aqui
```

### 2. Obtener usuario específico
```http
GET /users/{user_id}
Authorization: Bearer token_aqui
```

### 3. Actualizar perfil de usuario
```http
PUT /users/{user_id}
Authorization: Bearer token_aqui
Content-Type: application/json

{
    "full_name": "Juan Carlos Pérez",
    "password": "nuevaPassword456"
}
```

### 4. Eliminar cuenta de usuario
```http
DELETE /users/{user_id}
Authorization: Bearer token_aqui
```

## Configuración de Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Luego edita las variables según tu configuración:

```env
SECRET_KEY=tu-clave-secreta-muy-segura-de-al-menos-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://usuario:password@localhost:5432/habit_challenge
APP_NAME="Habit Challenge API"
DEBUG=false
```

## Ejecutar la aplicación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn api.app.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en:
- **Servidor:** http://localhost:8000
- **Documentación:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc

## Estructura de autenticación

1. **Registro:** El usuario se registra con email y contraseña
2. **Hash:** La contraseña se hashea con bcrypt antes de guardarse
3. **Login:** Se validan las credenciales y se genera un JWT
4. **Token:** El JWT contiene el email del usuario y tiempo de expiración
5. **Autenticación:** Para endpoints protegidos, incluir `Authorization: Bearer TOKEN`

## Características de seguridad

- ✅ Contraseñas hasheadas con bcrypt
- ✅ Tokens JWT con expiración
- ✅ Validación de email con pydantic
- ✅ Protección de endpoints sensibles
- ✅ Verificación de permisos (usuarios solo pueden modificar sus propios datos)
- ✅ Manejo de errores de autenticación
- ✅ Configuración centralizada con variables de entorno
