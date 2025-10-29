// Cargar widgets sociales dinámicamente
document.addEventListener('DOMContentLoaded', function() {
    // Solo cargar si el usuario está autenticado
    if (!document.querySelector('.twitter-layout')) {
        return;
    }

    // Cargar sugerencias de amigos
    loadFriendSuggestions();
    
    // Cargar trending topics
    loadTrendingTopics();
    
    // Cargar influencers
    loadInfluencers();
    
    // Agregar event listeners para posts
    setupPostEventListeners();
});

// Event listeners para los posts en el feed
function setupPostEventListeners() {
    // Click en contenido del post para ir al detalle
    document.querySelectorAll('.clickable-post').forEach(element => {
        element.addEventListener('click', function(e) {
            window.location.href = this.dataset.url;
        });
    });
    
    // Click en botón de comentarios
    document.querySelectorAll('.post-comment-action').forEach(element => {
        element.addEventListener('click', function(e) {
            e.stopPropagation();
            window.location.href = this.dataset.url;
        });
    });
    
    // Click en botón de editar
    document.querySelectorAll('.post-edit-action').forEach(element => {
        element.addEventListener('click', function(e) {
            e.stopPropagation();
            window.location.href = this.dataset.url;
        });
    });
    
    // Prevenir propagación en forms de like
    document.querySelectorAll('.like-form').forEach(form => {
        form.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    });
}

function loadFriendSuggestions() {
    fetch('/api/friend-suggestions/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('friend-suggestions');
            if (data.suggestions && data.suggestions.length > 0) {
                container.innerHTML = data.suggestions.slice(0, 3).map(user => `
                    <div class="user-suggestion">
                        <div class="user-suggestion-info">
                            <p class="user-suggestion-name">${user.username}</p>
                            <p class="user-suggestion-username">@${user.username}</p>
                        </div>
                        <button class="btn btn-follow" onclick="followUser(${user.user_id}, this)">
                            Seguir
                        </button>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="text-muted text-center">No hay sugerencias disponibles</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando sugerencias:', error);
            document.getElementById('friend-suggestions').innerHTML = 
                '<p class="text-muted text-center">Error al cargar sugerencias</p>';
        });
}

function loadTrendingTopics() {
    console.log('🔍 Cargando trending topics...');
    fetch('/api/trending-topics/')
        .then(response => {
            console.log('📡 Respuesta recibida:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('📊 Datos de tendencias:', data);
            const container = document.getElementById('trending-topics');
            if (data.trending && data.trending.length > 0) {
                console.log(`✅ Mostrando ${data.trending.length} tendencias`);
                
                // Logging detallado de cada tendencia
                data.trending.forEach((topic, index) => {
                    console.log(`  ${index + 1}. #${topic.name}: ${topic.count} posts`);
                });
                
                container.innerHTML = data.trending.slice(0, 5).map(topic => `
                    <div class="trending-item" onclick="window.location.href='/?type=${encodeURIComponent(topic.name)}'">
                        <div class="trending-topic">#${topic.name}</div>
                        <div class="trending-count">${topic.count} publicaciones</div>
                    </div>
                `).join('');
                
                console.log('✅ Widget de tendencias actualizado en el DOM');
            } else {
                console.log('⚠️ No hay tendencias para mostrar');
                container.innerHTML = '<p class="text-muted text-center">No hay tendencias aún</p>';
            }
        })
        .catch(error => {
            console.error('❌ Error cargando tendencias:', error);
            document.getElementById('trending-topics').innerHTML = 
                '<p class="text-muted text-center">Error al cargar tendencias</p>';
        });
}

function loadInfluencers() {
    fetch('/api/influencers/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('influencers-list');
            if (data.influencers && data.influencers.length > 0) {
                container.innerHTML = data.influencers.slice(0, 3).map(user => `
                    <div class="user-suggestion">
                        <div class="user-suggestion-info">
                            <p class="user-suggestion-name">${user.username}</p>
                            <p class="user-suggestion-username">${user.followers} seguidores</p>
                        </div>
                        <a href="/profile/${user.username}/" class="btn btn-sm btn-outline-primary">
                            Ver perfil
                        </a>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="text-muted text-center">No hay datos disponibles</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando influencers:', error);
            document.getElementById('influencers-list').innerHTML = 
                '<p class="text-muted text-center">Error al cargar influencers</p>';
        });
}

function followUser(userId, button) {
    fetch(`/api/follow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            button.textContent = 'Siguiendo';
            button.classList.remove('btn-follow');
            button.classList.remove('btn-outline-primary');
            button.classList.add('btn-following');
            button.classList.add('btn-outline-secondary');
            button.onclick = (e) => {
                e.stopPropagation();
                unfollowUser(userId, button);
            };
            
            // Recargar sugerencias de amigos
            loadFriendSuggestions();
        } else {
            const errorMsg = data.error || 'No se pudo seguir al usuario';
            console.error('Error en follow:', errorMsg);
            alert(`No se pudo seguir al usuario: ${errorMsg}`);
        }
    })
    .catch(error => {
        console.error('Error siguiendo usuario:', error);
        alert(`Error al seguir usuario: ${error.message}`);
    });
}

function unfollowUser(userId, button) {
    fetch(`/api/unfollow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            button.textContent = 'Seguir';
            button.classList.remove('btn-following');
            button.classList.remove('btn-outline-secondary');
            button.classList.add('btn-follow');
            button.classList.add('btn-outline-primary');
            button.onclick = (e) => {
                e.stopPropagation();
                followUser(userId, button);
            };
            
            // Recargar sugerencias de amigos
            loadFriendSuggestions();
        } else {
            const errorMsg = data.error || 'No se pudo dejar de seguir al usuario';
            console.error('Error en unfollow:', errorMsg);
            alert(`No se pudo dejar de seguir: ${errorMsg}`);
        }
    })
    .catch(error => {
        console.error('Error dejando de seguir:', error);
        alert(`Error al dejar de seguir: ${error.message}`);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
