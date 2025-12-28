# Acortes.cl - Portafolio Personal

Sitio web personal desarrollado con Django que presenta un portafolio profesional con información sobre experiencia, habilidades, proyectos personales y un formulario de contacto.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Despliegue](#despliegue)
- [Estructura de URLs](#estructura-de-urls)
- [Archivos Estáticos](#archivos-estáticos)
- [Logging](#logging)

## 📝 Descripción

Este proyecto es un sitio web personal que funciona como portafolio profesional. Permite a los visitantes conocer información sobre el desarrollador, su experiencia laboral, habilidades técnicas, proyectos personales y proporciona un formulario de contacto funcional.

## ✨ Características

- **Páginas principales:**
  - Página de inicio con hero section y acceso rápido
  - Sobre mí (Quién Soy)
  - Experiencia profesional
  - Habilidades técnicas
  - Proyectos personales
  - Formulario de contacto

- **Funcionalidades:**
  - Formulario de contacto con validación
  - Envío de emails mediante SMTP
  - Modo oscuro (Dark Mode)
  - Diseño responsive
  - Archivos estáticos optimizados con WhiteNoise
  - Sistema de logging configurado
  - Soporte multiidioma (Español/Inglés)

## 🛠 Tecnologías Utilizadas

- **Backend:**
  - Django 5.2.4
  - Python 3.13
  - SQLite3 (base de datos)

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
  - Font Awesome (iconos)

- **Herramientas y Librerías:**
  - python-dotenv (gestión de variables de entorno)
  - WhiteNoise (servicio de archivos estáticos)
  - Gunicorn (servidor WSGI para producción)

## 📁 Estructura del Proyecto

```
acortes_cl/
├── acortes_cl/          # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py      # Configuración principal
│   ├── urls.py          # URLs principales
│   ├── wsgi.py          # Configuración WSGI
│   └── asgi.py          # Configuración ASGI
│
├── app/                 # Aplicación principal
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py         # Formularios (ContactForm)
│   ├── models.py        # Modelos (actualmente vacío)
│   ├── views.py         # Vistas de la aplicación
│   ├── urls.py          # URLs de la aplicación
│   │
│   ├── templates/       # Plantillas HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── experience.html
│   │   ├── skills.html
│   │   ├── personal_projects.html
│   │   └── contact.html
│   │
│   └── static/          # Archivos estáticos
│       ├── css/
│       │   └── styles.css
│       ├── js/
│       │   └── darkmode.js
│       ├── images/
│       │   ├── front_img.jpeg
│       │   └── profile.jpeg
│       └── files/       # PDFs y documentos
│
├── staticfiles/         # Archivos estáticos recopilados (producción)
├── logs/               # Archivos de log
│   └── django.log
├── venv/               # Entorno virtual
├── db.sqlite3          # Base de datos SQLite
├── manage.py           # Script de administración Django
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.13 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

### Pasos de Instalación

1. **Clonar el repositorio** (si está en un repositorio Git):
```bash
git clone <url-del-repositorio>
cd acortes_cl
```

2. **Crear un entorno virtual**:
```bash
python3 -m venv venv
```

3. **Activar el entorno virtual**:
   - En Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
   - En Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Instalar las dependencias**:
```bash
pip install -r requirements.txt
```

5. **Aplicar migraciones** (si hay modelos):
```bash
python manage.py migrate
```

6. **Crear un superusuario** (opcional, para acceder al admin):
```bash
python manage.py createsuperuser
```

## ⚙️ Configuración

### Variables de Entorno

El proyecto utiliza variables de entorno para configuraciones sensibles. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Configuración de Debug
DEBUG=False

# Configuración de Email (Producción)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion
DEFAULT_FROM_EMAIL=tu_email@gmail.com
CONTACT_EMAIL=email_destino@gmail.com
```

**Nota:** Para Gmail, necesitarás generar una "Contraseña de aplicación" en lugar de usar tu contraseña normal. Ve a tu cuenta de Google > Seguridad > Verificación en 2 pasos > Contraseñas de aplicaciones.

### Configuración de Hosts Permitidos

En `settings.py`, el proyecto está configurado para los siguientes hosts:
- `149.50.150.195` (IP del servidor)
- `acortesv.cl`
- `www.acortesv.cl`
- `localhost`
- `127.0.0.1`

Ajusta `ALLOWED_HOSTS` según tus necesidades.

### Configuración de Email

El proyecto tiene dos configuraciones de email:

- **Desarrollo (DEBUG=True):** Usa el backend de consola, los emails se muestran en la terminal.
- **Producción (DEBUG=False):** Usa SMTP real con las credenciales del archivo `.env`.

## 🎯 Uso

### Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El sitio estará disponible en `http://127.0.0.1:8000/`

### Recopilar Archivos Estáticos

Para producción, recopila los archivos estáticos:

```bash
python manage.py collectstatic
```

Esto copiará todos los archivos estáticos a la carpeta `staticfiles/`.

### Acceder al Panel de Administración

Navega a `http://127.0.0.1:8000/admin/` y usa las credenciales del superusuario creado.

## 🌐 Despliegue

### Configuración para Producción

1. **Asegúrate de tener `DEBUG=False`** en tu archivo `.env`

2. **Recopila archivos estáticos**:
```bash
python manage.py collectstatic
```

3. **Usa Gunicorn como servidor WSGI**:
```bash
gunicorn acortes_cl.wsgi:application --bind 0.0.0.0:8000
```

4. **Configura un servidor web** (Nginx recomendado) como proxy inverso.

### Ejemplo de Configuración Nginx

```nginx
server {
    listen 80;
    server_name acortesv.cl www.acortesv.cl;

    location /static/ {
        alias /ruta/al/proyecto/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔗 Estructura de URLs

El proyecto define las siguientes rutas:

| URL | Vista | Nombre | Descripción |
|-----|-------|--------|-------------|
| `/` | `index` | `index` | Página de inicio |
| `/about/` | `about` | `about` | Sobre mí / Quién soy |
| `/experience/` | `experience` | `experience` | Experiencia profesional |
| `/skills/` | `skills` | `skills` | Habilidades técnicas |
| `/personal_projects/` | `personal_projects` | `personal_projects` | Proyectos personales |
| `/contact/` | `contact` | `contact` | Formulario de contacto |
| `/admin/` | - | - | Panel de administración Django |

## 📦 Archivos Estáticos

Los archivos estáticos se organizan en:

- **CSS:** `app/static/css/styles.css` - Estilos principales
- **JavaScript:** `app/static/js/darkmode.js` - Funcionalidad de modo oscuro
- **Imágenes:** `app/static/images/` - Imágenes del sitio
- **Archivos:** `app/static/files/` - PDFs y documentos descargables

En producción, los archivos se sirven desde `staticfiles/` mediante WhiteNoise.

## 📊 Logging

El proyecto tiene configurado un sistema de logging que registra:

- **Nivel INFO:** Operaciones normales, envíos de email exitosos
- **Nivel ERROR:** Errores en el envío de emails y otras excepciones

Los logs se guardan en:
- **Archivo:** `logs/django.log`
- **Consola:** Salida estándar durante desarrollo

### Formato de Logs

```
{levelname} {asctime} {module} {process:d} {thread:d} {message}
```

## 🔒 Seguridad

- **CSRF Protection:** Habilitado por defecto en Django
- **Secret Key:** Debe estar en variables de entorno en producción
- **DEBUG:** Deshabilitado en producción
- **ALLOWED_HOSTS:** Configurado para restringir hosts permitidos

## 📝 Formulario de Contacto

El formulario de contacto (`ContactForm`) incluye:

- **Validaciones:**
  - Nombre: mínimo 2 caracteres
  - Email: formato válido
  - Mensaje: mínimo 10 caracteres
  - Asunto: opcional

- **Funcionalidad:**
  - Envía emails mediante SMTP
  - Registra intentos de envío en logs
  - Muestra mensajes de éxito/error al usuario
  - Incluye información del remitente (IP, host) en el email

## 🌍 Internacionalización

El proyecto está configurado para soportar múltiples idiomas:

- **Idioma por defecto:** Español de Chile (`es-cl`)
- **Idiomas disponibles:** Español (`es`), Inglés (`en`)
- **Zona horaria:** `America/Santiago`

## 📄 Licencia

Este proyecto es de uso personal.

## 👤 Autor

Desarrollado como portafolio personal.

## 🤝 Contribuciones

Este es un proyecto personal, pero las sugerencias son bienvenidas.

## 📞 Contacto

Para más información, utiliza el formulario de contacto en el sitio web.

---

**Última actualización:** 2024

