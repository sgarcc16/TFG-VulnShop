# VulnShop - Entorno controlado de pentesting web

## Descripción del proyecto

VulnShop es un proyecto desarrollado como parte del Trabajo de Fin de Grado en Ingeniería Informática de la Universidad de León.

El objetivo del proyecto es diseñar, implementar y evaluar un entorno controlado para estudiar vulnerabilidades de aplicaciones web y la automatización parcial de auditorías de seguridad.

Para ello se ha desarrollado una aplicación web de comercio electrónico mediante Python y Flask denominada **VulnShop**, sobre la que se han introducido deliberadamente diez escenarios de seguridad representativos de las categorías del **OWASP Top 10:2025**.

El proyecto incluye además:

- despliegue reproducible mediante Docker;
- un laboratorio virtualizado formado por una máquina Kali Linux y una máquina Ubuntu Server;
- una auditoría manual de los escenarios vulnerables;
- una herramienta propia en Python para automatizar tareas de reconocimiento, enumeración y comprobación de seguridad;
- generación automática de informes;
- comparación entre los resultados obtenidos manualmente y mediante la herramienta automática.

> **Advertencia:** VulnShop contiene vulnerabilidades introducidas deliberadamente y debe utilizarse exclusivamente en entornos controlados, aislados y autorizados.

---

## Objetivos del proyecto

Los principales objetivos del Trabajo de Fin de Grado son:

1. Desarrollar una aplicación web funcional sobre la que puedan incorporarse escenarios de seguridad controlados.
2. Implementar diez escenarios representativos de las categorías del OWASP Top 10:2025.
3. Preparar un entorno reproducible mediante Docker.
4. Construir un laboratorio de pentesting formado por una máquina atacante y una máquina objetivo.
5. Realizar una auditoría manual sobre los escenarios implementados.
6. Desarrollar una herramienta propia en Python para automatizar parte del proceso de auditoría.
7. Comparar los resultados del pentesting manual con los obtenidos automáticamente.
8. Mantener trazabilidad de las diferentes versiones utilizadas durante el desarrollo y las pruebas.
9. Corregir posteriormente los escenarios vulnerables y comprobar la eficacia de las medidas aplicadas.

---

## Tecnologías utilizadas

| Tecnología | Utilización |
|---|---|
| Python | Desarrollo de VulnShop y de la herramienta automática |
| Flask | Framework de la aplicación web |
| Jinja | Generación de plantillas HTML |
| HTML / CSS | Interfaz de usuario |
| SQLite | Persistencia de datos |
| Docker | Contenerización y reproducción del entorno |
| Oracle VirtualBox | Virtualización del laboratorio |
| Kali Linux | Máquina atacante |
| Ubuntu Server | Máquina objetivo |
| Nmap | Reconocimiento de puertos y servicios |
| Requests | Comunicaciones HTTP de la herramienta automática |
| SSH | Acceso autorizado para determinadas comprobaciones internas |
| Git | Control de versiones |
| GitHub | Repositorio remoto del proyecto |

---

## Ramas y versiones de referencia

El proyecto utiliza diferentes puntos del historial de Git para separar las fases del desarrollo.

### `master`

Rama utilizada como referencia funcional de VulnShop.

Puntos de referencia relevantes:

- `secure-baseline` — commit `11f2895`
- `secure-baseline-ui` — commit `2987498`

El commit `2987498` corresponde a la versión funcional de referencia utilizada para comparar el comportamiento normal de la aplicación con los escenarios vulnerables.

### `vulnerable-lab`

Rama destinada al laboratorio deliberadamente vulnerable.

Versiones relevantes:

- commit `2476a42`: versión vulnerable de VulnShop utilizada durante las pruebas manuales y automáticas;
- commit `db6ff01`: incorporación al repositorio de la herramienta automática de pentesting utilizada en el capítulo de automatización del TFG.

---

## Escenarios vulnerables implementados

La rama `vulnerable-lab` incorpora diez escenarios deliberadamente inseguros.

| Categoría OWASP Top 10:2025 | Escenario implementado |
|---|---|
| A01 - Broken Access Control | IDOR sobre pedidos |
| A02 - Security Misconfiguration | Exposición de configuración interna |
| A03 - Software Supply Chain Failures | Dependencias sin versiones fijadas |
| A04 - Cryptographic Failures | Almacenamiento de contraseñas mediante MD5 |
| A05 - Injection | SQL Injection |
| A06 - Insecure Design | Manipulación del precio desde el cliente |
| A07 - Authentication Failures | Enumeración de usuarios |
| A08 - Software or Data Integrity Failures | Manipulación de un cupón |
| A09 - Security Logging and Alerting Failures | Ausencia de registro de intentos fallidos |
| A10 - Mishandling of Exceptional Conditions | Comportamiento fail-open ante una excepción |

Los escenarios se encuentran delimitados dentro del laboratorio y no pretenden representar de forma exhaustiva todas las vulnerabilidades incluidas dentro de cada categoría de OWASP.

---

## Estructura del proyecto

```text
TFG-VulnShop/
│
├── app.py
├── init_db.py
├── init_lab.py
├── check_dependencies.py
├── requirements.txt
├── requirements-lab-insecure.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
│
├── templates/
│   └── ...
│
├── static/
│   └── style.css
│
└── pentest-tool/
    ├── main.py
    ├── requirements.txt
    │
    └── modules/
        ├── __init__.py
        ├── reconnaissance.py
        ├── web_enum.py
        ├── vulnerability_checks.py
        ├── internal_checks.py
        └── reporting.py
```

---

## Aplicación VulnShop

VulnShop simula una aplicación básica de comercio electrónico.

Entre sus funcionalidades se encuentran:

- registro de usuarios;
- inicio y cierre de sesión;
- gestión de perfiles;
- catálogo de productos;
- búsqueda de productos;
- realización de pedidos;
- consulta del historial de pedidos;
- gestión administrativa de usuarios y productos.

Sobre estas funcionalidades se han incorporado los escenarios vulnerables descritos anteriormente.

---

## Despliegue mediante Docker

### Requisitos

Para desplegar VulnShop es necesario disponer de:

- Git;
- Docker;
- un terminal desde el que ejecutar los comandos.

### Clonar el repositorio

```bash
git clone https://github.com/sgarcc16/TFG-VulnShop.git
cd TFG-VulnShop
```

### Seleccionar la rama vulnerable

```bash
git switch vulnerable-lab
```

### Construir la imagen

Desde el directorio raíz:

```bash
docker build -t vulnshop-lab .
```

### Ejecutar el contenedor

La aplicación Flask utiliza el puerto `5000`.

Un ejemplo de ejecución local es:

```bash
docker run --rm -d --name vulnshop-lab-container -p 127.0.0.1:5000:5000 vulnshop-lab
```

En el laboratorio del TFG, la aplicación se ejecuta dentro de la máquina Ubuntu Server y se accede desde Kali Linux a través de la red interna configurada para las pruebas.

### Consultar los registros

```bash
docker logs vulnshop-lab-container
```

Para seguir la salida en tiempo real:

```bash
docker logs -f vulnshop-lab-container
```

### Detener el contenedor

```bash
docker stop vulnshop-lab-container
```

---

## Inicialización del laboratorio

El proyecto incluye scripts destinados a preparar los datos utilizados durante las pruebas.

`init_db.py` se utiliza para preparar la estructura principal de la base de datos y los datos funcionales de VulnShop.

`init_lab.py` prepara los datos específicos necesarios para reproducir los escenarios del laboratorio, incluyendo cuentas, productos y pedidos utilizados durante las comprobaciones.

Para recuperar un estado conocido después de realizar pruebas que hayan modificado la aplicación, el procedimiento utilizado durante el TFG consiste en reconstruir el entorno a partir de un contenedor nuevo y regenerar los datos necesarios.

---

## Laboratorio virtualizado

El entorno utilizado durante las pruebas está compuesto por dos máquinas virtuales ejecutadas mediante Oracle VirtualBox.

### Kali Linux

Actúa como máquina atacante y contiene las herramientas utilizadas durante el pentesting manual y la herramienta automática desarrollada para el proyecto.

Dirección utilizada en la red interna del laboratorio:

```text
192.168.56.10/24
```

### Ubuntu Server

Actúa como máquina objetivo.

En esta máquina se ejecutan Docker y el contenedor de VulnShop.

Dirección utilizada en la red interna:

```text
192.168.56.20/24
```

La aplicación puede ser accedida desde Kali Linux mediante:

```text
http://192.168.56.20:5000
```

Estas direcciones corresponden únicamente a la configuración utilizada durante el desarrollo del laboratorio.

---

# Herramienta automática de pentesting

La carpeta `pentest-tool/` contiene la herramienta Python desarrollada para automatizar determinadas fases de la auditoría.

La herramienta fue diseñada específicamente para VulnShop y no pretende funcionar como un escáner genérico de aplicaciones web.

## Estructura

```text
pentest-tool/
├── main.py
├── requirements.txt
└── modules/
    ├── __init__.py
    ├── reconnaissance.py
    ├── web_enum.py
    ├── vulnerability_checks.py
    ├── internal_checks.py
    └── reporting.py
```

### `main.py`

Punto de entrada de la herramienta y responsable de coordinar el flujo general de ejecución.

### `reconnaissance.py`

Contiene las tareas de reconocimiento inicial del sistema objetivo.

### `web_enum.py`

Realiza tareas relacionadas con el análisis y enumeración del servicio web.

### `vulnerability_checks.py`

Agrupa las comprobaciones realizadas principalmente mediante peticiones contra VulnShop.

### `internal_checks.py`

Contiene comprobaciones que requieren información interna del laboratorio y permite ejecutar operaciones autorizadas mediante SSH sobre la máquina objetivo.

### `reporting.py`

Organiza los resultados y genera los informes correspondientes a cada ejecución.

---

## Instalación de la herramienta

Desde la rama `vulnerable-lab`:

```bash
cd pentest-tool
```

Se recomienda utilizar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución de la herramienta

La herramienta recibe como argumento la dirección IP de la máquina objetivo.

En el laboratorio utilizado durante el TFG:

```bash
python main.py 192.168.56.20
```

La ejecución coordina las siguientes fases:

1. reconocimiento del sistema objetivo;
2. identificación de servicios;
3. análisis HTTP;
4. enumeración de rutas;
5. ejecución de las comprobaciones correspondientes a los diez escenarios de VulnShop;
6. generación de un informe con los resultados.

Algunas comprobaciones utilizan únicamente información accesible externamente mediante HTTP, mientras que otras requieren acceso SSH autorizado a la máquina objetivo para consultar información interna del laboratorio.

Por este motivo, la herramienta no debe considerarse un escáner estrictamente de caja negra.

---

## Pentesting manual

Antes de desarrollar la herramienta automática se realizó una auditoría manual desde Kali Linux contra la aplicación desplegada en Ubuntu Server.

Las pruebas incluyeron, entre otras tareas:

- reconocimiento mediante Nmap;
- peticiones HTTP;
- peticiones mediante `curl`;
- modificación de parámetros;
- comprobaciones de autenticación y autorización;
- consultas sobre datos internos del laboratorio;
- revisión de registros;
- comparación de las variantes funcionales y vulnerables.

El pentesting manual permitió validar previamente los diez escenarios implementados y obtener una referencia con la que comparar posteriormente la herramienta automática.

**Estado: completado.**

---

## Auditoría automática

La herramienta automática fue ejecutada contra el mismo laboratorio utilizado durante el pentesting manual.

Durante la validación integrada se identificaron los diez escenarios vulnerables incluidos dentro del alcance del proyecto.

Este resultado debe interpretarse únicamente dentro del entorno controlado de VulnShop, ya que las comprobaciones fueron desarrolladas específicamente para los escenarios conocidos del laboratorio.

**Estado: completado.**

---

## Comparación entre pentesting manual y auditoría automática

Los resultados obtenidos mediante ambas aproximaciones fueron comparados sobre el mismo conjunto de diez escenarios.

En la ejecución utilizada durante la evaluación:

| Escenario | Pentesting manual | Herramienta automática |
|---|---|---|
| A01 | Detectado | Detectado |
| A02 | Detectado | Detectado |
| A03 | Detectado | Detectado |
| A04 | Detectado | Detectado |
| A05 | Detectado | Detectado |
| A06 | Detectado | Detectado |
| A07 | Detectado | Detectado |
| A08 | Detectado | Detectado |
| A09 | Detectado | Detectado |
| A10 | Detectado | Detectado |

Estos resultados no implican que la herramienta tenga una capacidad general de detección equivalente a la de un pentesting manual.

La herramienta utiliza conocimiento previo del laboratorio y determinadas comprobaciones requieren acceso interno autorizado.

**Estado: completado.**

---

## Repetibilidad de las pruebas

Durante el desarrollo de la herramienta se prestó especial atención a evitar que las ejecuciones alterasen permanentemente el estado necesario para pruebas posteriores.

En particular, determinadas comprobaciones que modifican datos de VulnShop incorporan mecanismos para recuperar el estado previo después de su ejecución.

El objetivo es permitir que las comprobaciones automáticas puedan repetirse sobre condiciones conocidas.

---

## Corrección de vulnerabilidades

La siguiente fase del proyecto consiste en corregir los diez escenarios vulnerables implementados.

Para cada escenario se realizará la siguiente comprobación:

```text
Versión vulnerable → comportamiento inseguro
Versión corregida  → comportamiento seguro
```

Después se volverá a ejecutar la herramienta automática contra la versión corregida para comprobar que las condiciones vulnerables detectadas anteriormente han dejado de estar presentes.

**Estado: pendiente.**

---

## Estado actual del proyecto

### Completado

- [x] Desarrollo de VulnShop.
- [x] Implementación de los diez escenarios vulnerables.
- [x] Preparación del despliegue mediante Docker.
- [x] Inicialización automática de los datos del laboratorio.
- [x] Creación del laboratorio virtualizado.
- [x] Configuración de Kali Linux y Ubuntu Server.
- [x] Pentesting manual.
- [x] Desarrollo de la herramienta automática.
- [x] Integración de las comprobaciones A01-A10.
- [x] Generación automática de informes.
- [x] Validación integrada de la herramienta.
- [x] Comparación entre pentesting manual y auditoría automática.
- [x] Incorporación de la herramienta al repositorio.

### Pendiente

- [ ] Corregir los escenarios vulnerables A01-A10.
- [ ] Validar manualmente las correcciones.
- [ ] Ejecutar la herramienta automática contra la versión corregida.
- [ ] Documentar la comparación final entre versión vulnerable y corregida.
- [ ] Completar la documentación final del Trabajo de Fin de Grado.

---

## Advertencia de seguridad

**IMPORTANTE: VulnShop es una aplicación deliberadamente vulnerable.**

Este proyecto ha sido desarrollado exclusivamente con fines educativos y de investigación en ciberseguridad.

La aplicación contiene fallos de seguridad introducidos intencionadamente y no debe utilizarse en entornos de producción.

El laboratorio debe ejecutarse únicamente sobre infraestructura propia, controlada, aislada y autorizada.

No debe exponerse directamente a Internet ni utilizarse para realizar pruebas contra sistemas de terceros sin autorización.

---

## Repositorio

Repositorio del proyecto:

https://github.com/sgarcc16/TFG-VulnShop

Ramas principales:

- `master`: versión funcional de referencia.
- `vulnerable-lab`: versión utilizada para el laboratorio vulnerable y la herramienta automática.

---

## Autor

**Samuel García Calvo**

Trabajo de Fin de Grado en Ingeniería Informática  
Universidad de León
