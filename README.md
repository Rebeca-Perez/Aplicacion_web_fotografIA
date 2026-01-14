# 📸 FotografIA — Asistente de fotografía

FotografIA es una aplicación web que integra un LLM especializado en fotografía con un backend en Flask y una base de datos PostgreSQL para almacenar el historial de conversaciones.

## 🚀 Descripción

La aplicación permite a los usuarios:  

- Realizar preguntas sobre fotografía (técnica, equipos, estilos, consejos).  
- Obtener respuestas generadas por un modelo LLM configurado como experto en fotografía.  
- Guardar automáticamente cada interacción (pregunta, respuesta, modelo y fecha).  
- Consultar el historial de conversaciones desde la interfaz web.

El modelo está restringido al dominio de la fotografía, evitando desviaciones temáticas y respondiendo de forma breve cuando el usuario insiste fuera de contexto.

## 🧠 Características principales

- Backend con Flask

- Integración con LLM (llama-3.3-70b-versatile)

- Persistencia de datos con PostgreSQL + SQLAlchemy

- Historial de conversaciones consultable

- Frontend ligero en HTML, CSS y JavaScript

- Gestión segura de credenciales mediante variables de entorno

- Proyecto preparado para Docker y despliegue en la nube (Render)

## 🛠️ Tecnologías utilizadas

- Python 3.12  
- Flask  
- SQLAlchemy  
- PostgreSQL  
- LLM API   
- HTML / CSS / JavaScript  
- Docker (opcional)  
- GitHub  

## 📂 Estructura del proyecto

```
Aplicacion_web_fotografIA/
│
├── app.py                # Aplicación Flask
├── requirements.txt      # Dependencias del proyecto
├── .gitignore            # Archivos con contenido sensible (.env)
├── dockerfile
├── README.md
├── templates/
│   └── index.html        # Interfaz web
├── tests/
│   └── test_api.py       # Tests de endpoints
└── data/
    └── database.sql      # Esquema de la base de datos
```   
    
## ⚙️ Configuración

1. Clona el repositorio:  
```
git clone <url-del-repositorio>
cd nombre-del-proyecto
```
2. Instala las dependencias:  
```
pip install -r requirements.txt
```
3. Crea un archivo `.env` con las variables necesarias:  
```
DATABASE_URL=...
GROQ_API_KEY=...
```

## ▶️ Ejecución  
```
python app.py
```
La aplicación estará disponible en:  
```
http://localhost:5000
```

## 🧪 Endpoints principales

* `POST /query` → Enviar una pregunta al LLM
* `GET /historial` → Obtener el historial de conversaciones

## 🧪 Tests

Los tests de la API están definidos en:  
* tests/test_api.py

Ejecutar con:  
* pip install pytest
* pytest

## ☁️ Despliegue

https://fotografia-llm.onrender.com

Las credenciales y configuraciones sensibles se gestionan exclusivamente mediante variables de entorno.

## 👩‍💻 Autor

Rebeca Perez