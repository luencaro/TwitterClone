#!/bin/bash

# Script de inicialización del proyecto TwitterClone con Neo4j

echo "🚀 Inicializando TwitterClone con Neo4j..."

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python3 encontrado${NC}"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creando entorno virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
else
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
fi

# Activar entorno virtual
echo -e "${YELLOW}🔌 Activando entorno virtual...${NC}"
source venv/bin/activate

# Instalar dependencias
echo -e "${YELLOW}📚 Instalando dependencias...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencias instaladas${NC}"
else
    echo -e "${RED}❌ Error instalando dependencias${NC}"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Creando archivo .env...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Por favor, edita el archivo .env con tus credenciales de Neo4j${NC}"
    echo -e "${YELLOW}⚠️  Especialmente NEO4J_PASSWORD${NC}"
else
    echo -e "${GREEN}✓ Archivo .env ya existe${NC}"
fi

# Verificar si existe la base de datos SQLite
if [ ! -f "db.sqlite3" ]; then
    echo -e "${YELLOW}🗄️  Creando base de datos SQLite...${NC}"
    python manage.py migrate
    echo -e "${GREEN}✓ Base de datos SQLite creada${NC}"
    
    echo -e "${YELLOW}👤 Creando superusuario...${NC}"
    echo "Por favor, ingresa los datos del superusuario:"
    python manage.py createsuperuser
else
    echo -e "${GREEN}✓ Base de datos SQLite ya existe${NC}"
fi

# Verificar conexión a Neo4j
echo -e "${YELLOW}🔗 Verificando conexión a Neo4j...${NC}"
python -c "from blog.neo4j_connection import init_neo4j_connection; init_neo4j_connection()" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Conexión a Neo4j exitosa${NC}"
    
    # Preguntar si desea migrar datos
    read -p "¿Deseas migrar los datos existentes a Neo4j? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}📊 Migrando datos a Neo4j...${NC}"
        python manage.py migrate_to_neo4j --clear
        echo -e "${GREEN}✓ Datos migrados a Neo4j${NC}"
    fi
else
    echo -e "${RED}❌ No se pudo conectar a Neo4j${NC}"
    echo -e "${YELLOW}Asegúrate de que Neo4j esté corriendo y las credenciales en .env sean correctas${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✨ Inicialización completada${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "Para iniciar el servidor:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}python manage.py runserver${NC}"
echo ""
echo -e "Visita: ${GREEN}http://localhost:8000${NC}"
echo ""
