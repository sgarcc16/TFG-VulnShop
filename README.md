# VulnShop - Entorno controlado de pentesting web

## Descripción del proyecto

VulnShop es un proyecto desarrollado como parte del Trabajo de Fin de Grado en Ingeniería Informática de la Universidad de León.

El objetivo principal del proyecto es desarrollar un entorno controlado y reproducible para realizar pruebas de penetración (pentesting) sobre aplicaciones web.

Para ello, se ha desarrollado una aplicación web utilizando Python y Flask, en la que se introducen deliberadamente diferentes vulnerabilidades de seguridad tomando como referencia OWASP Top 10.

El proyecto también contempla el desarrollo de una herramienta propia en Python para automatizar determinadas fases de una auditoría de seguridad, la realización de pruebas manuales, la comparación de los resultados obtenidos y la posterior corrección de las vulnerabilidades implementadas.

El entorno utiliza Docker para facilitar el despliegue de la aplicación y permitir su ejecución en un entorno controlado.

---

## Objetivos del proyecto

Los principales objetivos del Trabajo de Fin de Grado son:

1. Desarrollar una aplicación web que contenga vulnerabilidades de seguridad introducidas deliberadamente.
2. Implementar diferentes escenarios de vulnerabilidad basados en OWASP Top 10.
3. Crear un entorno de pruebas controlado y reproducible mediante Docker.
4. Desarrollar una herramienta en Python para automatizar tareas de reconocimiento, enumeración y detección de vulnerabilidades.
5. Realizar una auditoría de seguridad manual sobre la aplicación.
6. Comparar los resultados obtenidos mediante el análisis manual y automatizado.
7. Corregir las vulnerabilidades implementadas.
8. Comprobar la eficacia de las medidas correctoras aplicadas.

---

## Tecnologías utilizadas

Las principales tecnologías utilizadas en el proyecto son:

| Tecnología | Utilización |
|---|---|
| Python 3.12 | Lenguaje de programación de la aplicación |
| Flask | Framework para el desarrollo web |
| HTML | Estructura de las páginas web |
| CSS | Diseño de la interfaz |
| Docker | Contenerización de la aplicación |
| Git | Control de versiones |
| GitHub | Almacenamiento y gestión del código fuente |

---

## Aplicación web vulnerable

VulnShop es una aplicación web desarrollada específicamente para servir como objetivo de pruebas de penetración.

La aplicación contiene vulnerabilidades introducidas deliberadamente para permitir su identificación, análisis y explotación dentro de un entorno autorizado.

El objetivo es reproducir diferentes problemas de seguridad que pueden aparecer en aplicaciones web reales y estudiar su funcionamiento.

La aplicación permitirá realizar las siguientes actividades:

- Identificación de vulnerabilidades web.
- Ejecución de pruebas de penetración controladas.
- Análisis del comportamiento de la aplicación ante diferentes ataques.
- Evaluación de herramientas de detección automática.
- Comparación entre auditorías manuales y automatizadas.
- Corrección de las vulnerabilidades identificadas.

### Vulnerabilidades implementadas

**Apartado pendiente de documentación.**

Se incorporará una descripción de las vulnerabilidades implementadas, indicando su funcionamiento, localización dentro de la aplicación y relación con las categorías de OWASP Top 10.

---

## Estructura del proyecto

Los principales archivos y directorios del proyecto son:

```text
TFG-VulnShop/
│
├── app.py
├── init_db.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
│
├── templates/
│
└── static/
```

### Descripción de los archivos

- **app.py:** archivo principal de la aplicación Flask. Contiene la lógica de funcionamiento de la aplicación web.

- **init_db.py:** script utilizado para inicializar la base de datos de la aplicación.

- **requirements.txt:** contiene las dependencias de Python necesarias para ejecutar el proyecto.

- **Dockerfile:** define las instrucciones necesarias para construir la imagen Docker de VulnShop.

- **.dockerignore:** especifica los archivos y directorios que deben excluirse del contexto de construcción de Docker.

- **templates/:** contiene las plantillas HTML utilizadas para generar las páginas de la aplicación.

- **static/:** contiene los recursos estáticos utilizados por la interfaz web.

---

## Instalación y ejecución mediante Docker

La aplicación está preparada para ejecutarse mediante Docker.

Esto permite construir una imagen que contiene Python, las dependencias necesarias y el código de la aplicación.

### 1. Requisitos previos

Para ejecutar el proyecto es necesario disponer de:

- Git.
- Docker instalado y en funcionamiento.
- Un terminal desde el que ejecutar los comandos.

No es necesario instalar Python ni Flask directamente en el equipo anfitrión, ya que estas dependencias se incluyen dentro de la imagen Docker.

### 2. Clonar el repositorio

Descargar el código fuente mediante el siguiente comando:

```bash
git clone https://github.com/sgarcc16/TFG-VulnShop.git
```

Acceder al directorio del proyecto:

```bash
cd TFG-VulnShop
```

### 3. Seleccionar la rama del laboratorio vulnerable

El desarrollo del laboratorio vulnerable se realiza en la rama `vulnerable-lab`.

Para cambiar a esta rama:

```bash
git switch vulnerable-lab
```

### 4. Construir la imagen Docker

Desde el directorio raíz del proyecto, donde se encuentra el archivo `Dockerfile`, ejecutar:

```bash
docker build -t vulnshop .
```

Este comando construye una imagen Docker denominada `vulnshop`.

Durante el proceso se realizan las siguientes operaciones:

1. Se utiliza como imagen base `python:3.12-slim`.
2. Se establece `/app` como directorio de trabajo.
3. Se copia el archivo `requirements.txt`.
4. Se instalan las dependencias necesarias mediante `pip`.
5. Se copia el código fuente de la aplicación.
6. Se configura el puerto 5000 como puerto expuesto por la imagen.

### 5. Ejecutar el contenedor

Una vez construida la imagen, iniciar el contenedor mediante:

```bash
docker run --rm -d --name vulnshop -p 127.0.0.1:5000:5000 vulnshop
```

Este comando realiza las siguientes operaciones:

- `--rm`: elimina automáticamente el contenedor cuando se detiene.
- `-d`: ejecuta el contenedor en segundo plano.
- `--name vulnshop`: asigna el nombre `vulnshop` al contenedor.
- `-p 127.0.0.1:5000:5000`: publica el puerto 5000 del contenedor únicamente en la interfaz local del equipo.
- `vulnshop`: especifica la imagen que se utilizará.

La aplicación se inicia mediante el comando definido en el Dockerfile:

```bash
python init_db.py && exec flask --app app run --host=0.0.0.0 --port=5000
```

En primer lugar, se ejecuta el script `init_db.py`, encargado de inicializar la base de datos.

Si este proceso finaliza correctamente, se inicia el servidor Flask escuchando en el puerto 5000 del contenedor.

### 6. Acceder a la aplicación

Una vez iniciado correctamente el contenedor, abrir un navegador web y acceder a:

http://localhost:5000

La aplicación estará disponible desde el propio equipo en el que se ejecuta Docker.

**Importante:** el acceso indicado corresponde a una ejecución local. La aplicación no debe exponerse directamente a Internet.

### 7. Consultar los registros del contenedor

Para comprobar el funcionamiento de la aplicación y consultar posibles errores:

```bash
docker logs vulnshop
```

Para visualizar los registros en tiempo real:

```bash
docker logs -f vulnshop
```

### 8. Detener el contenedor

Para detener la aplicación:

```bash
docker stop vulnshop
```

Debido a la opción `--rm`, el contenedor se eliminará automáticamente después de detenerse.

La imagen Docker permanecerá disponible y podrá utilizarse para iniciar un nuevo contenedor.

---

## Configuración de Docker

El proyecto utiliza el siguiente Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && exec flask --app app run --host=0.0.0.0 --port=5000"]
```

### Funcionamiento

La imagen parte de una versión reducida de Python 3.12.

Durante su construcción se instalan las dependencias indicadas en `requirements.txt` y se copia el código de la aplicación al directorio `/app`.

Cuando se inicia el contenedor, se ejecuta automáticamente el script de inicialización de la base de datos y, si finaliza correctamente, se arranca el servidor Flask.

El uso de Docker permite mantener las dependencias de la aplicación dentro del contenedor y facilita la reproducción del entorno en otros equipos compatibles.

---

## Automatización del pentesting

Una de las siguientes fases del proyecto consistirá en desarrollar una herramienta propia en Python para automatizar determinadas tareas de una auditoría de seguridad.

Entre las funcionalidades previstas se encuentran:

- Reconocimiento inicial del objetivo.
- Enumeración de recursos y servicios.
- Detección de determinadas vulnerabilidades web.
- Recopilación de los resultados del análisis.

La herramienta estará orientada al laboratorio desarrollado y permitirá estudiar las posibilidades y limitaciones de la automatización de pruebas de seguridad.

**Estado: pendiente de desarrollo.**

---

## Pentesting manual

Además de la herramienta automática, se realizará una auditoría manual sobre la aplicación vulnerable.

Esta auditoría permitirá analizar las vulnerabilidades implementadas mediante técnicas de pentesting y comprobar su comportamiento.

El objetivo es disponer de resultados obtenidos manualmente que puedan compararse posteriormente con los generados por la herramienta automática.

**Estado: pendiente de realización.**

---

## Comparación entre pentesting manual y automatizado

Una vez realizadas ambas auditorías, se compararán los resultados obtenidos.

Los principales aspectos que se pretende analizar son:

- Número de vulnerabilidades detectadas.
- Tipos de vulnerabilidades identificadas.
- Diferencias entre los resultados.
- Posibles falsos positivos y falsos negativos.
- Tiempo necesario para realizar las pruebas.
- Limitaciones de cada procedimiento.

Esta comparación permitirá evaluar el funcionamiento de la herramienta desarrollada y analizar las diferencias entre las pruebas manuales y automatizadas.

**Estado: pendiente de realización.**

---

## Corrección de vulnerabilidades

La última fase del proyecto consistirá en corregir las vulnerabilidades introducidas deliberadamente en la aplicación.

Para cada vulnerabilidad se documentará:

1. Descripción de la vulnerabilidad.
2. Código o funcionalidad afectada.
3. Procedimiento utilizado para detectarla.
4. Posibles consecuencias de su explotación.
5. Modificaciones realizadas para corregirla.
6. Comprobación de la eficacia de la corrección.

De esta forma, el proyecto permitirá estudiar el proceso completo de identificación, análisis y corrección de vulnerabilidades web.

**Estado: pendiente de desarrollo.**

---

## Estado actual del proyecto

El Trabajo de Fin de Grado se encuentra actualmente en desarrollo.

### Trabajo realizado

- [x] Creación del repositorio GitHub.
- [x] Desarrollo inicial de la aplicación web con Python y Flask.
- [x] Preparación del laboratorio vulnerable.
- [x] Implementación inicial de vulnerabilidades deliberadas.
- [x] Creación del Dockerfile.
- [x] Preparación de la configuración de Docker.
- [x] Configuración del proceso de inicialización de la base de datos.
- [x] Organización del código mediante Git.

### Trabajo pendiente

- [ ] Completar la documentación de las vulnerabilidades implementadas.
- [ ] Desarrollar la herramienta automática de pentesting.
- [ ] Realizar la auditoría manual.
- [ ] Comparar los resultados del pentesting manual y automatizado.
- [ ] Corregir las vulnerabilidades implementadas.
- [ ] Comprobar las correcciones realizadas.
- [ ] Completar la memoria del Trabajo de Fin de Grado.

---

## Advertencia de seguridad

**IMPORTANTE: VulnShop es una aplicación deliberadamente vulnerable.**

Este proyecto ha sido desarrollado exclusivamente con fines educativos y de investigación en ciberseguridad.

La aplicación contiene fallos de seguridad introducidos intencionadamente y no debe utilizarse en entornos de producción.

Se recomienda ejecutar el laboratorio únicamente en entornos controlados, aislados y autorizados.

No debe exponerse directamente a Internet ni utilizarse para realizar pruebas sobre sistemas de terceros sin autorización.

---

## Autor

Trabajo de Fin de Grado en Ingeniería Informática.

Universidad de León.

---

## Referencias

- OWASP Top 10
- Documentación oficial de Flask
- Documentación oficial de Docker
