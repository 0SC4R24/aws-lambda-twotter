# Práctica 3: Twitter en AWS (Lambda)

El siguiente ejercicio está pensado para poner en práctica los conocimientos de AWS Lambda/EC2/S3 adquiridos hasta el momento.
El alumno deberá impementar un programa usando los servicios deamazon, que simule una aplicación tipo red social/Twitter.
Se deberá implementar una base de datos,funciones lambda necesarias y páginas web que den los servicios especificados a continuación.
El ejercicioestá dividido en varias partes, cada una de ellas cubrirá una de las herramientas vistas.
Notas a tener en cuenta:

- No se ha usado RDS por su alto coste, pero se deja libertad al alumno el hecho de usarlo eimplementar las bases de datos con esta herramienta
- Las bases de datos usadas en los ejemplos de clase estaban basadas en mysql, y alojadas dentrode ordenadores EC2.
- Se deja libertad para cambiar el tipo de base de datos y alojamiento siempreque sea una máquina con acceso en internet.

## Indice

- [Enunciado](#enunciado)
- [Partes opcionales](#partes-opcionales)
- [Autores](#autores)

## Enunciado

Se pide implementar una página web que permita publicar comentarios con archivos multimedia adjuntos (videos o imágenes), gestionar usuarios y propiedad de sus comentarios/archivos, listar comentariospropios y de otros usuarios, crear listas de usuarios seguidores/seguidos, realizar respuestas a mensajesde otros usuarios.
Las funcionalidades principales serán las siguientes:

- Login y registro de usuarios
- Por cada usuario, acceso a una página web que permita crear comentarios y subir ficheros de video/imágenes adjuntas
- Listado de comentarios propios y reproducción de adjuntos

## Partes opcionales

- Gestión de usuarios seguidos:
- Opción de búsqueda de usuarios
- Opción de añadir un usuario a una lista de “seguidos”
- Mostrar mensajes de usuarios seguidos en una página web, ordenados por fecha depublicación
- Gestión de respuestas a mensajes
- Votación positiva/negativa (like/dislike)
- Respuesta a un mensaje
- Seguridad en accesos a páginas (se deja al alumno implementar sistemas tipo “cookies”, sesiones,passwords, videos/posts privados privados....)

# Autores

- Adrian Toral
- Oscar Viudez
