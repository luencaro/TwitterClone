#!/bin/bash

echo "🚀 Setup Neo4j para TwitterClone"
echo "================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker no está instalado${NC}"
    echo "Instala Docker primero: sudo dnf install docker"
    exit 1
fi

# Verificar si Docker está corriendo
if ! sudo systemctl is-active --quiet docker; then
    echo -e "${YELLOW}⚠️  Docker no está corriendo. Iniciando...${NC}"
    sudo systemctl start docker
    sleep 2
fi

echo -e "${GREEN}✓ Docker está corriendo${NC}"

# Verificar si ya existe el contenedor
if sudo docker ps -a | grep -q neo4j-twitterclone; then
    echo -e "${YELLOW}⚠️  El contenedor neo4j-twitterclone ya existe${NC}"
    
    # Verificar si está corriendo
    if sudo docker ps | grep -q neo4j-twitterclone; then
        echo -e "${GREEN}✓ Neo4j ya está corriendo${NC}"
    else
        echo -e "${YELLOW}Iniciando contenedor existente...${NC}"
        sudo docker start neo4j-twitterclone
        sleep 3
        echo -e "${GREEN}✓ Neo4j iniciado${NC}"
    fi
else
    echo -e "${YELLOW}📦 Creando nuevo contenedor de Neo4j...${NC}"
    sudo docker run \
        --name neo4j-twitterclone \
        -p 7474:7474 -p 7687:7687 \
        -d \
        -v $HOME/neo4j/data:/data \
        -v $HOME/neo4j/logs:/logs \
        -e NEO4J_AUTH=neo4j/NuevaNeo4jPass2024!Segura \
        neo4j:5.14
    
    echo -e "${YELLOW}Esperando que Neo4j inicie (30 segundos)...${NC}"
    sleep 30
    echo -e "${GREEN}✓ Neo4j creado e iniciado${NC}"
fi

# Verificar logs
echo ""
echo -e "${YELLOW}📋 Últimas líneas del log de Neo4j:${NC}"
sudo docker logs --tail 5 neo4j-twitterclone

# Actualizar archivo .env
echo ""
echo -e "${YELLOW}⚙️  Actualizando archivo .env...${NC}"
cd /home/luencaro/Programing/My\ Repositories/College/Base\ de\ Datos/TwitterClone

if [ -f .env ]; then
    # Backup del .env original
    cp .env .env.backup
    
    # Actualizar password
    sed -i 's/NEO4J_PASSWORD=.*/NEO4J_PASSWORD=password123/' .env
    echo -e "${GREEN}✓ Archivo .env actualizado${NC}"
    echo -e "${YELLOW}  (Backup guardado en .env.backup)${NC}"
else
    echo -e "${YELLOW}⚠️  Archivo .env no existe. Creando desde .env.example...${NC}"
    cp .env.example .env
    sed -i 's/NEO4J_PASSWORD=.*/NEO4J_PASSWORD=password123/' .env
    echo -e "${GREEN}✓ Archivo .env creado${NC}"
fi

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✨ Neo4j configurado correctamente${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "Accesos:"
echo -e "  📊 Neo4j Browser: ${YELLOW}http://localhost:7474${NC}"
echo -e "  🌐 Django App:    ${YELLOW}http://localhost:8000${NC}"
echo ""
echo -e "Credenciales Neo4j:"
echo -e "  Usuario:  ${YELLOW}neo4j${NC}"
echo -e "  Password: ${YELLOW}password123${NC}"
echo ""
echo -e "Próximos pasos:"
echo -e "  1. ${YELLOW}python manage.py migrate_to_neo4j --clear${NC}"
echo -e "  2. ${YELLOW}python manage.py runserver${NC}"
echo -e "  3. Visita ${YELLOW}http://localhost:8000/friends/${NC}"
echo ""
