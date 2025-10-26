"""
Módulo para gestionar la conexión con Neo4j
"""
from neomodel import config, db
from django.conf import settings
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Variable global para rastrear si ya se inicializó
_connection_initialized = False


def init_neo4j_connection():
    """
    Inicializa la conexión con Neo4j usando neomodel
    """
    global _connection_initialized
    
    # Si ya se inicializó, no reinicializar
    if _connection_initialized:
        return True
    
    # Obtener credenciales de variables de entorno o usar valores por defecto
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
    
    print(f"DEBUG: Conectando a Neo4j con usuario: {neo4j_user}")
    
    # Configurar la conexión
    connection_url = f"{neo4j_uri.replace('bolt://', 'bolt://' + neo4j_user + ':' + neo4j_password + '@')}"
    config.DATABASE_URL = connection_url
    
    # Verificar la conexión
    try:
        db.cypher_query("RETURN 1")
        _connection_initialized = True
        print("✓ Conexión exitosa con Neo4j")
        return True
    except Exception as e:
        print(f"✗ Error al conectar con Neo4j: {e}")
        return False


def get_neo4j_driver():
    """
    Retorna una instancia del driver de Neo4j para queries personalizadas
    """
    from neo4j import GraphDatabase
    
    neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
    neo4j_password = os.getenv('NEO4J_PASSWORD', 'password')
    
    return GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))


def close_neo4j_connection():
    """
    Cierra la conexión con Neo4j
    """
    global _connection_initialized
    try:
        db.close_connection()
        _connection_initialized = False
        print("✓ Conexión con Neo4j cerrada")
    except Exception as e:
        print(f"✗ Error al cerrar conexión con Neo4j: {e}")


# Inicializar conexión automáticamente al importar el módulo
init_neo4j_connection()
