
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

## API Reference

### Authentication

- Register

    Ruta: `/auth/register`

    Metodo: `POST`

    Desc: `Crear un usuario en la DB`

    JSON Body  : `{
    "email": string,
    "password": string
    }`

    Response: `{
        "message": string,
        "user_id": string,
        "email": string
    }`

- Login

    Ruta: `/auth/login`

    Metodo: `POST`

    Desc: `Generar un JWT`

    JSON Body  : `{
    "email": string,
    "password": string
    }`

    Response: `{
        "message": string,
        "access_token": string,
        "token_type": string
    }`

### Users CRUD

- Get all users

    Ruta: `/users`

    Metodo: `GET`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Retornar todos los usuarios registrados`

    Response: `{
        "results": [
            {
                "id": string,
                "email": string,
                "password": string,
                "created_at": string datetime,
                "deleted": bool,
                "shortened_urls": [
                    {
                        "id": string,
                        "raw_url": string,
                        "shorten_url": string,
                        "created_by": string,
                        "created_at": string,
                        "deleted": bool
                    }
                ]
            }
        ]
    }`

- Get user by ID

    Ruta: `/users/{user_id}`

    URL Params: `{"user_id": string}`

    Metodo: `GET`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Retornar un usuario especifico`

    Response: `{
                "id": string,
                "email": string,
                "password": string,
                "created_at": string datetime,
                "deleted": bool,
                "shortened_urls": [
                    {
                        "id": string,
                        "raw_url": string,
                        "shorten_url": string,
                        "created_by": string,
                        "created_at": string,
                        "deleted": bool
                    }
                ]
            }`
    
- Delete

    Ruta: `/users/{user_id}`

    URL Params: `{"user_id": string}`

    Metodo: `DELETE`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Soft delete a un usuario especifico`

    Response: `{
        "message": string,
        "user_id": string
    }`    

### URL's CRUD

- Get all url's

    Ruta: `/urls`

    Metodo: `GET`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Retornar todas las url's registradas`

    Response: `{
        "results": [
         {
            "raw_url": string,
            "shorten_url": string,
            "created_by": string,
            "created_at": string,
            "deleted": bool
         }
        ]
    }`

- Redirect by shortened ID

    Ruta: `/short/{url_short_id}`

    URL Params: `{"url_short_id": string}`

    Metodo: `GET`

    Desc: `Redirecciona a la URL original mediante la acortada`

- Create shortened URL

    Ruta: `/urls`

    Metodo: `POST`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Crea una URL acortada`

    JSON Body: `{
        "raw_url": string
    }`

    Response: `{
         {
            "message": string,
            "shortened_url": string,
            "original_url": string,
         }
    }`

- Delete shortened URL

    Ruta: `/urls/{url_short_id}`

    Metodo: `DELETE`

    Headers: `Authorization: Bearer {$ACCESS_TOKEN}`

    Desc: `Soft delete a una URL`

    Response: `{
         {
            "message": string,
         }
    }`

