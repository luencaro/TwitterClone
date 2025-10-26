# Queries Cypher Útiles para TwitterClone

## 📊 Estadísticas Generales

### Contar todos los nodos por tipo
```cypher
MATCH (n)
RETURN labels(n) as tipo, count(*) as cantidad
ORDER BY cantidad DESC;
```

### Contar todas las relaciones por tipo
```cypher
MATCH ()-[r]->()
RETURN type(r) as tipo_relacion, count(*) as cantidad
ORDER BY cantidad DESC;
```

### Ver estructura completa del grafo (limitado)
```cypher
MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 100;
```

## 👥 Consultas de Usuarios

### Usuarios más activos (con más posts)
```cypher
MATCH (u:UserNode)-[:POSTED]->(p:PostNode)
WITH u, count(p) as post_count
RETURN u.username, post_count
ORDER BY post_count DESC
LIMIT 10;
```

### Usuarios más influyentes (con más seguidores)
```cypher
MATCH (u:UserNode)<-[:FOLLOWS]-(follower)
WITH u, count(follower) as follower_count
RETURN u.username, follower_count
ORDER BY follower_count DESC
LIMIT 10;
```

### Usuarios que más siguen a otros
```cypher
MATCH (u:UserNode)-[:FOLLOWS]->(followed)
WITH u, count(followed) as following_count
RETURN u.username, following_count
ORDER BY following_count DESC
LIMIT 10;
```

### Usuarios con más amigos
```cypher
MATCH (u:UserNode)-[:FRIEND_OF]-(friend)
WITH u, count(DISTINCT friend) as friend_count
RETURN u.username, friend_count
ORDER BY friend_count DESC
LIMIT 10;
```

## 🤝 Análisis de Relaciones

### Amigos sugeridos para un usuario específico
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})-[:FRIEND_OF]->(friend)-[:FRIEND_OF]->(suggestion)
WHERE NOT (u)-[:FRIEND_OF]->(suggestion) AND u <> suggestion
WITH suggestion, count(*) as common_friends
RETURN suggestion.username, common_friends
ORDER BY common_friends DESC
LIMIT 10;
```

### Usuarios para seguir basados en intereses comunes
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})-[:INTERESTED_IN]->(i:InterestNode)<-[:INTERESTED_IN]-(suggestion)
WHERE NOT (u)-[:FOLLOWS]->(suggestion) AND u <> suggestion
WITH suggestion, count(DISTINCT i) as common_interests
RETURN suggestion.username, common_interests
ORDER BY common_interests DESC
LIMIT 10;
```

### Intereses comunes entre dos usuarios
```cypher
MATCH (u1:UserNode {username: 'usuario1'})-[:INTERESTED_IN]->(i:InterestNode)<-[:INTERESTED_IN]-(u2:UserNode {username: 'usuario2'})
RETURN i.name as interes_comun;
```

### Camino más corto entre dos usuarios
```cypher
MATCH path = shortestPath(
  (u1:UserNode {username: 'usuario1'})-[*]-(u2:UserNode {username: 'usuario2'})
)
RETURN path;
```

### Grado de separación entre usuarios
```cypher
MATCH path = shortestPath(
  (u1:UserNode {username: 'usuario1'})-[:FRIEND_OF*]-(u2:UserNode {username: 'usuario2'})
)
RETURN length(path) as grados_separacion;
```

## 📝 Consultas de Posts

### Posts más populares (con más likes)
```cypher
MATCH (u:UserNode)-[:LIKES]->(p:PostNode)
WITH p, count(u) as likes_count
MATCH (author:UserNode)-[:POSTED]->(p)
RETURN author.username, p.content, likes_count
ORDER BY likes_count DESC
LIMIT 10;
```

### Posts más comentados
```cypher
MATCH (c:CommentNode)-[:COMMENT_ON]->(p:PostNode)
WITH p, count(c) as comment_count
MATCH (author:UserNode)-[:POSTED]->(p)
RETURN author.username, p.content, comment_count
ORDER BY comment_count DESC
LIMIT 10;
```

### Posts recientes
```cypher
MATCH (u:UserNode)-[:POSTED]->(p:PostNode)
RETURN u.username, p.content, p.created_at
ORDER BY p.created_at DESC
LIMIT 20;
```

### Posts de un usuario específico
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})-[:POSTED]->(p:PostNode)
RETURN p.content, p.created_at
ORDER BY p.created_at DESC;
```

## 🏷️ Consultas de Intereses

### Intereses más populares (trending)
```cypher
MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode)
WITH i, count(p) as post_count
RETURN i.name, post_count
ORDER BY post_count DESC
LIMIT 10;
```

### Posts por interés específico
```cypher
MATCH (p:PostNode)-[:TAGGED_WITH]->(i:InterestNode {name: 'nombre_interes'})
MATCH (author:UserNode)-[:POSTED]->(p)
RETURN author.username, p.content, p.created_at
ORDER BY p.created_at DESC;
```

### Usuarios interesados en un tema
```cypher
MATCH (u:UserNode)-[:INTERESTED_IN]->(i:InterestNode {name: 'nombre_interes'})
RETURN u.username;
```

### Intereses de un usuario
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})-[:INTERESTED_IN]->(i:InterestNode)
RETURN i.name;
```

## 🔍 Análisis Avanzado

### Detectar comunidades (usuarios altamente conectados)
```cypher
CALL gds.louvain.stream('myGraph')
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).username AS username, communityId
ORDER BY communityId;
```

### PageRank de usuarios (influencia)
```cypher
CALL gds.pageRank.stream({
  nodeProjection: 'UserNode',
  relationshipProjection: 'FOLLOWS'
})
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).username AS username, score
ORDER BY score DESC
LIMIT 10;
```

### Análisis de red de un usuario
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})
OPTIONAL MATCH (u)-[:FOLLOWS]->(following)
OPTIONAL MATCH (u)<-[:FOLLOWS]-(follower)
OPTIONAL MATCH (u)-[:FRIEND_OF]-(friend)
OPTIONAL MATCH (u)-[:POSTED]->(post)
OPTIONAL MATCH (u)-[:INTERESTED_IN]->(interest)
RETURN 
    count(DISTINCT following) as siguiendo,
    count(DISTINCT follower) as seguidores,
    count(DISTINCT friend) as amigos,
    count(DISTINCT post) as posts,
    count(DISTINCT interest) as intereses;
```

### Feed personalizado (posts de quien sigo)
```cypher
MATCH (u:UserNode {username: 'nombre_usuario'})
OPTIONAL MATCH (u)-[:FOLLOWS]->(followed:UserNode)-[:POSTED]->(p:PostNode)
OPTIONAL MATCH (u)-[:POSTED]->(own_post:PostNode)
WITH collect(DISTINCT p) + collect(DISTINCT own_post) as all_posts
UNWIND all_posts as post
WHERE post IS NOT NULL
MATCH (author:UserNode)-[:POSTED]->(post)
RETURN author.username, post.content, post.created_at
ORDER BY post.created_at DESC
LIMIT 50;
```

### Usuarios similares a mí (basado en intereses)
```cypher
MATCH (me:UserNode {username: 'mi_usuario'})-[:INTERESTED_IN]->(i:InterestNode)<-[:INTERESTED_IN]-(similar:UserNode)
WHERE me <> similar
WITH similar, count(i) as common_interests
ORDER BY common_interests DESC
LIMIT 10
MATCH (similar)-[:INTERESTED_IN]->(their_interests:InterestNode)
RETURN similar.username, common_interests, collect(their_interests.name) as sus_intereses;
```

## 🧹 Mantenimiento

### Eliminar todos los nodos y relaciones (¡CUIDADO!)
```cypher
MATCH (n)
DETACH DELETE n;
```

### Eliminar un tipo específico de nodo
```cypher
MATCH (n:PostNode)
DETACH DELETE n;
```

### Eliminar relaciones huérfanas
```cypher
MATCH ()-[r]->()
WHERE NOT exists((startNode(r))) OR NOT exists((endNode(r)))
DELETE r;
```

### Ver índices y constraints
```cypher
SHOW INDEXES;
SHOW CONSTRAINTS;
```

### Crear índices para mejor performance
```cypher
CREATE INDEX user_username IF NOT EXISTS FOR (u:UserNode) ON (u.username);
CREATE INDEX user_id IF NOT EXISTS FOR (u:UserNode) ON (u.user_id);
CREATE INDEX post_id IF NOT EXISTS FOR (p:PostNode) ON (p.post_id);
CREATE INDEX interest_name IF NOT EXISTS FOR (i:InterestNode) ON (i.name);
```

## 📈 Performance y Optimización

### Ver plan de ejecución de una query
```cypher
EXPLAIN
MATCH (u:UserNode)-[:POSTED]->(p:PostNode)
RETURN u.username, count(p);
```

### Analizar performance de una query
```cypher
PROFILE
MATCH (u:UserNode)-[:POSTED]->(p:PostNode)
RETURN u.username, count(p);
```

### Estadísticas de la base de datos
```cypher
CALL dbms.queryJmx("org.neo4j:*") YIELD name, attributes
RETURN name, attributes;
```

## 🎯 Queries de Validación

### Verificar que todos los posts tienen autor
```cypher
MATCH (p:PostNode)
WHERE NOT exists((p)<-[:POSTED]-())
RETURN count(p) as posts_sin_autor;
```

### Verificar posts sin hashtags
```cypher
MATCH (p:PostNode)
WHERE NOT exists((p)-[:TAGGED_WITH]->())
RETURN count(p) as posts_sin_hashtags;
```

### Usuarios que no siguen a nadie
```cypher
MATCH (u:UserNode)
WHERE NOT exists((u)-[:FOLLOWS]->())
RETURN u.username;
```

## 💡 Tips

1. Usa `LIMIT` en queries exploratorias para no sobrecargar el navegador
2. Usa `EXPLAIN` y `PROFILE` para optimizar queries lentas
3. Crea índices en propiedades que uses frecuentemente en búsquedas
4. Para grafos grandes, considera usar Graph Data Science Library
5. Usa parámetros en lugar de valores hardcodeados para mejor performance

## 🔗 Ejecutar desde Python

```python
from neomodel import db

# Ejecutar query directa
query = """
MATCH (u:UserNode)
RETURN u.username, u.email
LIMIT 10
"""
results, meta = db.cypher_query(query)

# Con parámetros
query = """
MATCH (u:UserNode {username: $username})
RETURN u
"""
results, meta = db.cypher_query(query, {'username': 'mi_usuario'})
```
