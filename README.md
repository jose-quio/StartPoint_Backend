# Descubre AQP — Backend

API REST desarrollada con **FastAPI** que da soporte a la aplicación móvil *Descubre AQP*, una plataforma para el descubrimiento de lugares turísticos y recreativos en la ciudad de Arequipa, Perú.

## Contexto

El sistema permite a los usuarios explorar, buscar y recibir recomendaciones sobre lugares turísticos y recreativos de Arequipa (piscinas, termales, miradores, zonas campestres, entre otros). El backend expone los servicios que consume la aplicación Flutter, y gestiona cuatro roles de usuario:

- **Usuario registrado**: explora lugares, deja reseñas, marca favoritos y consulta al chatbot de recomendaciones.
- **Administrador de lugar**: registra y gestiona la información de los lugares que le pertenecen (horarios, precios, servicios, imágenes, ubicación).
- **Moderador**: aprueba o rechaza los lugares registrados antes de que sean visibles públicamente, garantizando la calidad de la información.
- **Visitante (sin cuenta)**: puede explorar lugares aprobados sin necesidad de registrarse.

### Características principales

- Autenticación y autorización basada en **JWT**, con control de acceso por rol.
- Gestión completa de lugares (CRUD), categorías, servicios, horarios e imágenes.
- Sistema de reseñas y calificaciones con promedio automático por lugar.
- Sistema de favoritos por usuario.
- Flujo de moderación (`pending` → `approved` / `rejected`) antes de publicar un lugar.
- **Chatbot conversacional** de recomendación, implementado con *function calling* sobre la API de **Groq** (modelo Llama 3.3 70B): el modelo interpreta el lenguaje natural del usuario y delega la búsqueda real a la base de datos, evitando que invente lugares inexistentes.
- **Sistema de recomendación basado en contenido** para la vista principal, que prioriza lugares según las categorías, servicios y rango de precio de los favoritos e historial de búsqueda del usuario.
- Almacenamiento de imágenes vía URLs de **Cloudinary** (la subida del archivo se realiza desde el cliente; el backend solo persiste la URL resultante).

### Stack tecnológico

| Componente | Tecnología |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy + Alembic (migraciones) |
| Base de datos | PostgreSQL (Neon) |
| Autenticación | JWT (python-jose) + bcrypt |
| IA conversacional | Groq API (Llama 3.3 70B, function calling) |
| Imágenes | Cloudinary (gestionado desde el cliente) |
| Despliegue | Docker sobre Render |

---

## Requisitos previos

- Python 3.11 o superior
- Cuenta en [Neon](https://neon.tech) (PostgreSQL gratuito) con la cadena de conexión lista
- Cuenta en [Groq Console](https://console.groq.com) con una API Key generada (formato `gsk_...`)
- Cuenta en [Cloudinary](https://cloudinary.com) (el backend solo necesita el `cloud_name`, la subida ocurre en el cliente)

---

## Puesta en marcha (entorno local)

### 1. Clonar el repositorio y crear entorno virtual

```bash
git clone <url-del-repositorio>
cd StartPoint_Backend
python -m venv venv
```

Activar el entorno virtual:

```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / macOS
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DATABASE_URL=postgresql://usuario:password@ep-xxxxx.neon.tech/nombre_bd?sslmode=require
SECRET_KEY=una_clave_secreta_larga_y_aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GROQ_API_KEY=gsk_tu_api_key_de_groq
CHATBOT_MODEL=llama-3.3-70b-versatile
```

> **Importante:** `DATABASE_URL` debe usar el prefijo `postgresql://` (no `postgres://`) y debe incluir `?sslmode=require`, que Neon exige.

### 4. Ejecutar las migraciones

```bash
alembic upgrade head
```

Esto crea todas las tablas necesarias (`users`, `places`, `categories`, `reviews`, `favorites`, `place_images`, `place_schedules`, `services`, `place_services`, `search_history`) en la base de datos configurada.

### 5. Levantar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

La API queda disponible en `http://127.0.0.1:8000`, y la documentación interactiva (Swagger) en:

```
http://127.0.0.1:8000/docs
```

### 6. Verificar que todo funciona

```
GET http://127.0.0.1:8000/health
```

Debe responder:
```json
{"status": "ok", "project": "Turismo Arequipa API"}
```

---

## Despliegue en producción (Render)

El proyecto incluye un `Dockerfile` listo para desplegar en [Render](https://render.com):

1. Sube el proyecto a un repositorio de GitHub.
2. En Render, crea un **New → Web Service**, seleccionando el repositorio y **Docker** como entorno de ejecución.
3. Configura las mismas variables de entorno del paso 3 anterior en la sección *Environment* de Render.
4. Define el **Health Check Path** como `/health`.
5. Despliega. El `Dockerfile` ejecuta automáticamente `alembic upgrade head` antes de levantar `uvicorn`, por lo que las migraciones se aplican en cada despliegue.

> Nota: el plan gratuito de Render "duerme" el servicio tras un periodo de inactividad. La primera petición después de ese periodo puede tardar de 30 a 60 segundos en responder mientras el contenedor se reactiva.

---

## Estructura del proyecto

```
app/
├── main.py                # Punto de entrada de la aplicación
├── core/                  # Configuración, seguridad (JWT), logging
├── db/                    # Conexión y base declarativa de SQLAlchemy
├── models/                # Modelos de datos (tablas)
├── schemas/                # Esquemas Pydantic (request/response)
├── crud/                   # Acceso a datos por entidad
├── services/                # Lógica de negocio (chatbot, recomendaciones)
└── api/v1/endpoints/        # Endpoints agrupados por recurso
alembic/                     # Migraciones de base de datos
```

## Roles y permisos (resumen)

| Acción | Visitante | Registrado | Admin de lugar | Moderador |
|---|:---:|:---:|:---:|:---:|
| Ver lugares aprobados | ✅ | ✅ | ✅ | ✅ |
| Registrarse / iniciar sesión | ✅ | — | — | — |
| Dejar reseñas / favoritos | ❌ | ✅ | ✅ | ✅ |
| Usar el chatbot | ❌ | ✅ | ✅ | ✅ |
| Crear / editar lugares propios | ❌ | ❌ | ✅ | ✅ |
| Aprobar / rechazar lugares | ❌ | ❌ | ❌ | ✅ |

> Los roles se asignan manualmente en la base de datos (`UPDATE users SET role = '...' WHERE email = '...'`) ya que el registro público solo crea usuarios con rol `registered`.