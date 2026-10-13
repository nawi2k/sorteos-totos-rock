# 🎁 Sorteos Instagram - Totos Rock Drugstore

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-Deployed-000000?style=for-the-badge&logo=vercel&logoColor=white)

Aplicación web full-stack diseñada para la gestión automatizada de sorteos transparentes y equitativos en Instagram, desarrollada a medida para el comercio **Totos Rock Drugstore**.

La plataforma permite extraer los comentarios de cualquier publicación pública de Instagram mediante un enlace directo, aplicando filtros de unicidad de usuario para evitar ventajas por comentarios múltiples y seleccionando ganadores de manera aleatoria.

---

## 🚀 Características Principales

- **Filtro Anti-Duplicados (1 Usuario = 1 Entrada):** Procesa el listado completo de comentarios y garantiza que cada cuenta participe exactamente una vez, independientemente de la cantidad de veces que haya comentado.
- **Sin Credenciales de Usuario:** Funciona con publicaciones públicas sin requerir inicios de sesión ni permisos de cuenta de Instagram.
- **Interfaz Intuitiva y Responsiva:** Diseño limpio adaptado para dispositivos móviles y escritorio con branding personalizado de *Totos Rock*.
- **Arquitectura Decoplada:** Separación clara entre el motor de extracción/API REST (Backend) y la interfaz de usuario (Frontend).

---

## 🛠️ Arquitectura y Tecnologías

### **Backend**
- **Lenguaje:** Python 3.12
- **Framework Web:** FastAPI (ASGI Server con Uvicorn)
- **Scraping / Data Extraction:** `instaloader`
- **Modelado de Datos:** Pydantic
- **CORS Middleware:** Habilitado para comunicación cross-origin segura.

### **Frontend**
- **Estructura y Estilos:** HTML5 & CSS3
- **Lógica de Cliente:** JavaScript Vanilla (ES6+) con Fetch API

---

## 📁 Estructura del Proyecto

```text
PaginaDeSorteosTotosRock/
├── backend/
│   ├── main.py              # Servidor FastAPI y endpoints
│   └── requirements.txt     # Dependencias del servidor Python
├── frontend/
│   ├── index.html           # Interfaz de usuario
│   ├── styles.css           # Hoja de estilos con branding
│   ├── app.js               # Consumo de API y lógica del sorteo
│   └── assets/              # Recursos gráficos (logos e imágenes)
├── .python-version          # Especificación de entorno para Render (3.12.8)
└── README.md                # Documentación del repositorio