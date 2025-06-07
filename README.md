
# Challenge: Acortador de URL's

## Ejecutar el proyecto

#### Dependencias minimas

Para poder ejecutar el proyecto, es necesario contar con Docker y Docker compose instalados en el sistema operativo, dado que la aplicacion entera esta montada sobre contenedores para asegurar la integridad del proyecto. 

Instalar Docker 👉🏼 https://docs.docker.com/get-started/get-docker/

Instalar Docker compose 👉🏼 https://docs.docker.com/compose/install/

#### Ejecutar el proyecto

Para poder ejecutar el proyecto, teniendo docker-compose instalado, es necesario ejecutar el siguiente comando **con permisos de administrador**.

`docker compose up --build`

El comando se va a encargar de:

- Buildear la imagen del proyecto
- Buildear la imagen de la instancia de PostgreSQL
- Ejecutar ambos en su correspondiente contenedor
- Ejecutar las migraciones a la base de datos con Alembic
- Correr los test unitarios

## Estructura de carpetas

`app/adapters/input` 👉🏼 Entradas a la APP (Controllers, HTTP)

`app/adapters/output` 👉🏼 Salidas de la APP (Repositorios)

`app/domain/ports/input` 👉🏼 Interfaces de los UseCases que mapean con los adapters de entrada

`app/domain/ports/output` 👉🏼 Interfaces de los Repositorios

`app/domain/services` 👉🏼 UseCases que heredan de su puerto de entrada correspondiente

## Referencia a la API

Por defecto, la APP levanta en el puerto 8000, por ende, el hostt es `http://localhost:8000/` 😉

📖 **Todos los endpoints, a excepcion de `/docs - /login - /register - /short` requieren indicar el JWT en el Authorization Header**

📚 Documentacion y Endpoints -> `/docs` 

## Project Overview

## ⚙ Tecnologías utilizadas
### 🧠 Framework: FastAPI
Elegí FastAPI por varias razones:

- Su sintaxis clara y minimalista permite desarrollar rápidamente.

- Ideal para proyectos con tiempos limitados gracias a su enrutamiento sencillo.

- Validación automática de datos mediante Pydantic y sus DTOs.

- Generación automática de errores en las solicitudes erroneas.

- Soporte de tipado estático.

- Documentación automatica con Swagger en la ruta `/docs`

- Lo que más destaco: inyección de dependencias con el módulo Depends, que permite mapear controladores con sus respectivos puertos de forma totalmente desacoplada.

- Familiaridad con la dependencia fastapi-limiter, útil para prevenir ataques DDoS y limitar múltiples peticiones en corto tiempo.

### 🗄️ Base de datos: PostgreSQL
Para la base de datos, opté por PostgreSQL:

- Necesitaba una base relacional para manejar relaciones claras entre entidades (usuarios y URLs acortadas).

- Preferí un esquema rígido para mantener integridad en los modelos.

- Utilicé Alembic para manejar las migraciones de manera eficiente y ordenada.

### 🔄 ORM: SQLAlchemy
- Elegí SQLAlchemy por las siguientes razones:

- Familiaridad previa y fácil implementación.

- Protección automática contra inyecciones SQL.

- Manejo explícito de transacciones.

- Soporta múltiples motores de bases de datos, permitiendo desacople del driver de PostgreSQL.

- Soporte robusto para relaciones entre tablas y claves foráneas.

### 🧱 Infraestructura y arquitectura
🧩 Arquitectura Hexagonal (Ports & Adapters)
Opté por este enfoque arquitectónico porque:

- FastAPI, junto con Depends, facilita un mapeo limpio entre puertos y adaptadores.

- Aisla completamente la lógica de negocio (dominio) de los detalles de infraestructura (bases de datos, frameworks, protocolos).

- Mejora la escalabilidad del sistema: es sencillo agregar funcionalidades sin afectar otras partes.

- El testeo es más simple porque el dominio no depende de ningún entorno externo.

- Favorece la legibilidad del código al separar claramente capas: dominio por un lado, infraestructura por otro.

- Es ideal para implementar Domain-Driven Design (DDD) de forma clara y facil.

### 💡 Solución al problema de los ShortID's

Primero, se recibe un UUID4 convertido a un número entero (int). Este número se divide repetidamente por 62, y en
cada iteración se toma el resto para buscar un carácter correspondiente en una cadena que representa el alfabeto Base62 (62 caracteres posibles).
Cada carácter obtenido se agrega a un array. Una vez finalizado el proceso, se invierte el array y se une en una cadena para formar
el ID. Luego, se retorna una porción del resultado final, limitada a la longitud deseada.

### 🔄 Extras

- Para ejecutar los test de integración

    - Situarse dentro de la carpeta raiz del proyecto

    - Iniciar un VENV

    - Instalar las dependencias con `pip install -r requirements.txt`

    - Ejecutar `python -m unittest discover app/tests/integration -v`


