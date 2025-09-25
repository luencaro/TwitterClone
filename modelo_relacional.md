# Modelo Relacional - Django Twitter Clone

```mermaid
erDiagram
    USER ||--o{ POST : author
    USER ||--o{ COMMENT : author
    USER ||--o{ PREFERENCE : user
    USER ||--o{ PROFILE : user
    USER ||--o{ FOLLOW : user
    USER ||--o{ FOLLOW : follow_user
    POST ||--o{ COMMENT : post_connected
    POST ||--o{ PREFERENCE : post
    PROFILE ||--o{ USER : user

    POST {
        int id PK
        text content
        datetime date_posted
        int likes
        int dislikes
    }
    COMMENT {
        int id PK
        text content
        datetime date_posted
    }
    PREFERENCE {
        int id PK
        int value
        datetime date
    }
    PROFILE {
        int id PK
        image image
    }
    FOLLOW {
        int id PK
        datetime date
    }
```

## Descripción de las tablas y relaciones

- **User**: Utiliza el modelo estándar de Django.
- **Profile**: Relación uno a uno con User. Almacena la imagen de perfil.
- **Post**: Relación muchos a uno con User (author). Representa los tweets.
- **Comment**: Relación muchos a uno con User (author) y Post (post_connected).
- **Preference**: Relación muchos a uno con User y Post. Guarda likes/dislikes.
- **Follow**: Relación muchos a uno con User (user) y User (follow_user). Representa seguidores y seguidos.
