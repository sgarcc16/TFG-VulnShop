# VulnShop - Aplicación web de referencia para un entorno de pentesting

## Descripción del proyecto

VulnShop es un proyecto desarrollado como parte del Trabajo de Fin de Grado en Ingeniería Informática de la Universidad de León.

El proyecto tiene como objetivo estudiar vulnerabilidades de aplicaciones web y la automatización parcial de auditorías de seguridad dentro de un entorno controlado.

La rama `master` contiene la versión funcional de referencia de VulnShop. Esta versión se utiliza como base para comparar el comportamiento normal de la aplicación con los escenarios vulnerables implementados posteriormente en la rama `vulnerable-lab`.

La aplicación ha sido desarrollada mediante Python y Flask y reproduce funcionalidades habituales de una aplicación de comercio electrónico.

---

## Funcionalidades principales

La versión funcional de VulnShop incluye:

- registro de usuarios;
- autenticación y cierre de sesión;
- gestión de perfiles;
- catálogo de productos;
- búsqueda de productos;
- realización de pedidos;
- historial de pedidos;
- consulta individual de pedidos;
- gestión administrativa de usuarios y productos.

Las comprobaciones de autenticación, autorización y validación se realizan en la lógica del servidor.

---

## Tecnologías utilizadas

| Tecnología | Utilización |
|---|---|
| Python | Lenguaje principal de desarrollo |
| Flask | Framework de la aplicación web |
| Jinja | Generación de plantillas HTML |
| HTML / CSS | Interfaz de usuario |
| SQLite | Persistencia de datos |
| Docker | Contenerización de la aplicación |
| Git | Control de versiones |
| GitHub | Repositorio remoto del proyecto |

---

## Estructura del proyecto

```text
TFG-VulnShop/
│
├── app.py
├── init_db.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
│
├── templates/
│   └── ...
│
└── static/
    └── style.css
```

### Archivos principales

- `app.py`: contiene la aplicación Flask y la lógica principal.
- `init_db.py`: inicializa la base de datos y los datos funcionales.
- `requirements.txt`: contiene las dependencias de Python.
- `Dockerfile`: define la imagen utilizada para ejecutar VulnShop.
- `.dockerignore`: excluye archivos innecesarios durante la construcción de la imagen.
- `templates/`: contiene las plantillas HTML.
- `static/`: contiene los recursos estáticos de la interfaz.

---

## Control de versiones

El proyecto mantiene separados los diferentes estados de desarrollo mediante Git.

La rama `master` conserva la versión funcional de referencia.

Puntos de referencia relevantes:

- `secure-baseline` — commit `11f2895`
- `secure-baseline-ui` — commit `2987498`

El commit `2987498` corresponde a la versión funcional utilizada como referencia durante la comparación con los escenarios vulnerables.

La rama `vulnerable-lab` contiene:

- los diez escenarios vulnerables del laboratorio;
- la configuración específica utilizada durante las pruebas;
- la herramienta automática de pentesting desarrollada para el TFG;
- los componentes utilizados durante la evaluación manual y automática.

---

## Instalación mediante Docker

### Requisitos

Para ejecutar VulnShop es necesario disponer de:

- Git;
- Docker;
- un terminal desde el que ejecutar los comandos.

### Clonar el repositorio

```bash
git clone https://github.com/sgarcc16/TFG-VulnShop.git
cd TFG-VulnShop
```

### Seleccionar la rama `master`

```bash
git switch master
```

### Construir la imagen

```bash
docker build -t vulnshop .
```

### Ejecutar el contenedor

```bash
docker run --rm -d --name vulnshop -p 127.0.0.1:5000:5000 vulnshop
```

La aplicación estará disponible en:

```text
http://localhost:5000
```

### Consultar los registros

```bash
docker logs vulnshop
```

### Detener el contenedor

```bash
docker stop vulnshop
```

---

## Relación con la rama vulnerable

La rama `master` se utiliza como versión funcional de referencia.

Para acceder al laboratorio vulnerable:

```bash
git switch vulnerable-lab
```

La rama `vulnerable-lab` incorpora los escenarios representativos del OWASP Top 10:2025 y la herramienta automática desarrollada para realizar comprobaciones sobre ellos.

El objetivo de mantener ambas ramas separadas es facilitar la trazabilidad y permitir comparar el comportamiento funcional de la aplicación con las variantes deliberadamente inseguras.

---

## Repositorio

Repositorio del proyecto:

https://github.com/sgarcc16/TFG-VulnShop

Ramas principales:

- `master`: versión funcional de referencia.
- `vulnerable-lab`: laboratorio vulnerable y herramienta automática.

---

## Advertencia de seguridad

La rama `master` corresponde a la versión funcional de referencia del proyecto.

La rama `vulnerable-lab` contiene vulnerabilidades introducidas deliberadamente con fines educativos y de investigación.

El laboratorio vulnerable debe utilizarse únicamente en infraestructura propia, aislada, controlada y autorizada.

No debe exponerse directamente a Internet ni utilizarse para realizar pruebas contra sistemas de terceros sin autorización.

---

## Autor

**Samuel García Calvo**

Trabajo de Fin de Grado en Ingeniería Informática  
Universidad de León
