# 📊 Modelo de Datos - TwitterClone con Neo4j

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    TwitterClone Application                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐                    ┌──────────────┐       │
│  │    Django    │◄──────────────────►│    Neo4j     │       │
│  │   (SQLite)   │                    │   (Grafos)   │       │
│  └──────────────┘                    └──────────────┘       │
│        │                                     │               │
│        │                                     │               │
│  ┌─────▼──────┐                    ┌────────▼──────┐       │
│  │ User Auth  │                    │ Social Graph  │       │
│  │ Sessions   │                    │ Posts         │       │
│  │ Admin      │                    │ Comments      │       │
│  └────────────┘                    │ Relationships │       │
│                                    └───────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## Modelo de Nodos en Neo4j

### 1. UserNode (Nodo de Usuario)

```
┌─────────────────────────────┐
│       UserNode              │
├─────────────────────────────┤
│ Properties:                 │
│ • user_id: Integer (PK)     │
│ • username: String (Unique) │
│ • email: String             │
│ • first_name: String        │
│ • last_name: String         │
│ • bio: String               │
│ • date_joined: DateTime     │
└─────────────────────────────┘
```

### 2. PostNode (Nodo de Publicación)

```
┌─────────────────────────────┐
│       PostNode              │
├─────────────────────────────┤
│ Properties:                 │
│ • post_id: Integer (PK)     │
│ • content: String           │
│ • created_at: DateTime      │
│ • updated_at: DateTime      │
└─────────────────────────────┘
```

### 3. CommentNode (Nodo de Comentario)

```
┌─────────────────────────────┐
│      CommentNode            │
├─────────────────────────────┤
│ Properties:                 │
│ • comment_id: Integer (PK)  │
│ • content: String           │
│ • created_at: DateTime      │
└─────────────────────────────┘
```

### 4. InterestNode (Nodo de Interés)

```
┌─────────────────────────────┐
│     InterestNode            │
├─────────────────────────────┤
│ Properties:                 │
│ • name: String (Unique)     │
│ • description: String       │
│ • created_at: DateTime      │
└─────────────────────────────┘
```

## Relaciones del Grafo

### Esquema Completo de Relaciones

```
                   ┌──────────────┐
        ┌──────────┤  UserNode    ├──────────┐
        │          └──────┬───────┘          │
        │                 │                  │
        │                 │                  │
    FOLLOWS           POSTED            FRIEND_OF
        │                 │                  │
        │                 │                  │
        ▼                 ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ UserNode │      │ PostNode │      │ UserNode │
  └──────────┘      └────┬─────┘      └──────────┘
                         │
                         │
                    TAGGED_WITH
                         │
                         ▼
                   ┌──────────────┐
                   │ InterestNode │
                   └──────────────┘
                   
        
  UserNode ──COMMENTED──► CommentNode ──COMMENT_ON──► PostNode
  
  UserNode ──LIKES──► PostNode
  
  UserNode ──INTERESTED_IN──► InterestNode
```

### Descripción de Relaciones

#### 1. POSTED
```
(UserNode)-[:POSTED]->(PostNode)
```
- **Descripción**: Usuario crea una publicación
- **Dirección**: Unidireccional
- **Cardinalidad**: Uno a muchos (un usuario puede crear muchos posts)
- **Propiedades**: Ninguna adicional

#### 2. FOLLOWS
```
(UserNode)-[:FOLLOWS]->(UserNode)
```
- **Descripción**: Usuario sigue a otro usuario
- **Dirección**: Unidireccional
- **Cardinalidad**: Muchos a muchos
- **Propiedades**: 
  - `since: DateTime` - Fecha desde que sigue

#### 3. FRIEND_OF
```
(UserNode)-[:FRIEND_OF]-(UserNode)
```
- **Descripción**: Relación de amistad bidireccional
- **Dirección**: Bidireccional
- **Cardinalidad**: Muchos a muchos
- **Propiedades**:
  - `since: DateTime` - Fecha de amistad
  - `status: String` - Estado (pending, accepted, rejected)

#### 4. LIKES
```
(UserNode)-[:LIKES]->(PostNode)
```
- **Descripción**: Usuario da "me gusta" a un post
- **Dirección**: Unidireccional
- **Cardinalidad**: Muchos a muchos
- **Propiedades**:
  - `liked_at: DateTime` - Fecha del like

#### 5. COMMENTED
```
(UserNode)-[:COMMENTED]->(CommentNode)
```
- **Descripción**: Usuario crea un comentario
- **Dirección**: Unidireccional
- **Cardinalidad**: Uno a muchos
- **Propiedades**: Ninguna adicional

#### 6. COMMENT_ON
```
(CommentNode)-[:COMMENT_ON]->(PostNode)
```
- **Descripción**: Comentario asociado a un post
- **Dirección**: Unidireccional
- **Cardinalidad**: Muchos a uno
- **Propiedades**: Ninguna adicional

#### 7. INTERESTED_IN
```
(UserNode)-[:INTERESTED_IN]->(InterestNode)
```
- **Descripción**: Usuario interesado en un tema
- **Dirección**: Unidireccional
- **Cardinalidad**: Muchos a muchos
- **Propiedades**: Ninguna adicional

#### 8. TAGGED_WITH
```
(PostNode)-[:TAGGED_WITH]->(InterestNode)
```
- **Descripción**: Post etiquetado con un hashtag/interés
- **Dirección**: Unidireccional
- **Cardinalidad**: Muchos a muchos
- **Propiedades**: Ninguna adicional

## Ejemplos de Patrones de Grafo

### Patrón 1: Red de Amigos
```
(Alice:UserNode)-[:FRIEND_OF]-(Bob:UserNode)-[:FRIEND_OF]-(Charlie:UserNode)
                                      │
                                      └─[:FRIEND_OF]─(Diana:UserNode)
```

### Patrón 2: Publicación con Interacciones
```
(Author:UserNode)-[:POSTED]->(Post:PostNode)
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
        [:LIKES]            [:COMMENT_ON]      [:TAGGED_WITH]
              │                   │                   │
              ▼                   ▼                   ▼
    (User1:UserNode)    (Comment:CommentNode)  (Interest:InterestNode)
    (User2:UserNode)          ▲
    (User3:UserNode)          │
                         [:COMMENTED]
                              │
                        (Commenter:UserNode)
```

### Patrón 3: Descubrimiento de Contenido
```
(User:UserNode)-[:INTERESTED_IN]->(Interest:InterestNode)
                                         ▲
                                         │
                                   [:TAGGED_WITH]
                                         │
                                   (Post:PostNode)
                                         │
                                     [:POSTED]
                                         │
                                   (Author:UserNode)
```

## Índices y Constraints

### Índices Necesarios
```cypher
// Índices para búsquedas rápidas
CREATE INDEX user_username IF NOT EXISTS FOR (u:UserNode) ON (u.username);
CREATE INDEX user_id IF NOT EXISTS FOR (u:UserNode) ON (u.user_id);
CREATE INDEX user_email IF NOT EXISTS FOR (u:UserNode) ON (u.email);
CREATE INDEX post_id IF NOT EXISTS FOR (p:PostNode) ON (p.post_id);
CREATE INDEX post_created IF NOT EXISTS FOR (p:PostNode) ON (p.created_at);
CREATE INDEX comment_id IF NOT EXISTS FOR (c:CommentNode) ON (c.comment_id);
CREATE INDEX interest_name IF NOT EXISTS FOR (i:InterestNode) ON (i.name);
```

### Constraints de Unicidad
```cypher
// Asegurar unicidad
CREATE CONSTRAINT user_id_unique IF NOT EXISTS FOR (u:UserNode) REQUIRE u.user_id IS UNIQUE;
CREATE CONSTRAINT username_unique IF NOT EXISTS FOR (u:UserNode) REQUIRE u.username IS UNIQUE;
CREATE CONSTRAINT post_id_unique IF NOT EXISTS FOR (p:PostNode) REQUIRE p.post_id IS UNIQUE;
CREATE CONSTRAINT interest_name_unique IF NOT EXISTS FOR (i:InterestNode) REQUIRE i.name IS UNIQUE;
```

## Queries Principales por Caso de Uso

### 1. Feed de Usuario
```cypher
// Obtener posts de usuarios que sigo + mis posts
MATCH (me:UserNode {user_id: $user_id})
OPTIONAL MATCH (me)-[:FOLLOWS]->(followed)-[:POSTED]->(post:PostNode)
OPTIONAL MATCH (me)-[:POSTED]->(my_post:PostNode)
WITH collect(DISTINCT post) + collect(DISTINCT my_post) as all_posts
UNWIND all_posts as p
WHERE p IS NOT NULL
RETURN p
ORDER BY p.created_at DESC
LIMIT 50
```

### 2. Sugerencias de Amigos
```cypher
// Amigos de amigos que no son mis amigos
MATCH (me:UserNode {user_id: $user_id})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(suggestion)
WHERE NOT (me)-[:FRIEND_OF]->(suggestion) AND me <> suggestion
WITH suggestion, count(*) as common_friends
RETURN suggestion
ORDER BY common_friends DESC
LIMIT 10
```

### 3. Trending Topics
```cypher
// Intereses más populares
MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode)
WHERE p.created_at > datetime() - duration('P7D') // Últimos 7 días
WITH i, count(p) as post_count
RETURN i
ORDER BY post_count DESC
LIMIT 10
```

### 4. Análisis de Influencia
```cypher
// Usuarios más influyentes por seguidores
MATCH (u:UserNode)<-[:FOLLOWS]-(follower)
WITH u, count(follower) as followers
RETURN u.username, followers
ORDER BY followers DESC
LIMIT 10
```

## Métricas de Performance

### Comparación: Grafo vs Relacional

| Operación | SQL (Relacional) | Cypher (Neo4j) | Ventaja |
|-----------|------------------|----------------|---------|
| Amigos en común | 3+ JOINs, O(n²) | Path matching, O(n) | Neo4j |
| 6 grados separación | Recursión compleja | shortestPath() | Neo4j |
| Posts de usuario | SELECT simple | MATCH simple | Similar |
| Feed personalizado | Múltiples JOINs | Pattern matching | Neo4j |
| Trending topics | GROUP BY pesado | Aggregate simple | Similar |

### Estimación de Complejidad

```
Operación                      SQL         Neo4j
─────────────────────────────  ──────────  ───────────
Buscar usuario                 O(log n)    O(1)
Posts de usuario               O(n)        O(k)
Amigos de usuario              O(n)        O(k)
Amigos en común                O(n²)       O(k)
Camino más corto              O(n³)       O(k log k)
Sugerencias basadas en grafo  O(n³)       O(k²)

Donde: n = total usuarios, k = conexiones promedio
```

## Escalabilidad

### Datos Estimados

| Escenario | Usuarios | Posts/día | Relaciones | Tamaño DB |
|-----------|----------|-----------|------------|-----------|
| Pequeño   | 1K       | 100       | 5K         | < 100 MB  |
| Mediano   | 100K     | 10K       | 500K       | ~2 GB     |
| Grande    | 1M       | 100K      | 5M         | ~20 GB    |
| Enterprise| 10M+     | 1M+       | 50M+       | 200+ GB   |

### Recomendaciones por Tamaño

**Pequeño (< 1K usuarios)**
- Hardware: 2 CPU, 4GB RAM
- Neo4j: Configuración default
- Backups: Diarios

**Mediano (100K usuarios)**
- Hardware: 4 CPU, 16GB RAM
- Neo4j: dbms.memory.heap.max_size=8G
- Backups: Cada 6 horas
- Considerar réplicas de lectura

**Grande (1M+ usuarios)**
- Hardware: 8+ CPU, 32+ GB RAM
- Neo4j Enterprise Edition
- Clustering y sharding
- Backups: Continuos
- CDN para estáticos

---

## 📈 Visualización del Grafo

Para visualizar el grafo completo en Neo4j Browser:

```cypher
// Vista general
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100

// Vista por tipo
MATCH path = (u:UserNode)-[:FRIEND_OF]-(f:UserNode)
RETURN path
LIMIT 50

// Subgrafo de un usuario
MATCH (u:UserNode {username: 'mi_usuario'})
CALL apoc.path.subgraphAll(u, {maxLevel: 2})
YIELD nodes, relationships
RETURN nodes, relationships
```

---

**Este modelo aprovecha las fortalezas de Neo4j para manejar eficientemente relaciones complejas en una red social.**
