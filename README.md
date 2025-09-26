

# Bases de Datos - Laboratorio 03: Aplicación de Gestión de Posts y Comentarios

Este repositorio contiene el desarrollo de una aplicación para la gestión de posts y comentarios, implementada como parte del Laboratorio 03 de la asignatura de Bases de Datos. El objetivo principal es afianzar los conocimientos en diseño y modelamiento de bases de datos relacionales.

## 🚀 Tecnologías Utilizadas

*   **Lenguaje de Programación:** Python
*   **Framework:** Django
*   **Motor de Base de Datos:** SQLite

## 📦 Estructura del Proyecto

El proyecto incluye un diseño detallado de la base de datos y scripts para su creación:

1.  **Diagrama Entidad-Relación (ERD):** Visualización de las entidades principales (Usuarios, Posts, Comentarios, Tipos de Post) y sus relaciones.
2.  **Modelo Relacional:** Especificación de tablas, atributos, tipos de datos, claves primarias y foráneas, y restricciones de integridad.
3.  **Script SQL:** Un script para la creación de las tablas de la base de datos.

## 💡 Funcionalidades de la Aplicación

La aplicación ofrece un menú interactivo con las siguientes funcionalidades principales:

*   **Operaciones CRUD para Usuarios:** Crear, ver, actualizar y eliminar usuarios.
*   **Operaciones CRUD para Posts:** Crear, ver, actualizar y eliminar posts (con eliminación en cascada de comentarios).
*   **Operaciones CRUD para Comentarios:** Añadir, ver, actualizar y eliminar comentarios.
*   **Operaciones CRUD para Tipos de Posts:** Crear, ver, actualizar y eliminar tipos de post.
*   **Búsqueda de Posts:** Buscar posts por tipo, tema, autor y palabras clave.
*   **Visualización de Posts Completos:** Ver el contenido completo de un post y todos sus comentarios asociados.
*   **Listado de Usuarios y Cantidad de Posts:** Un listado que muestra cada usuario y el número total de posts que ha publicado.





### Restricciones Implementadas

*   Un post solo puede ser editado o eliminado por su autor.
*   Un comentario solo puede ser editado o eliminado por su autor.

## 🤝 Integrantes del Grupo

*   Juan Aguirre
*   Luis Cabarcas
*   Andres España
*   Jose Menco
*   Camilo Vargas

## 🗓️ Fecha del Laboratorio

26 de septiembre de 2025

---
