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
    
    // Click en botón de seguir en posts
    document.querySelectorAll('.btn-follow-post').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const userId = this.dataset.userId;
            followUser(userId, this);
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
    fetch('/api/trending-topics/')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('trending-topics');
            if (data.trending && data.trending.length > 0) {
                container.innerHTML = data.trending.slice(0, 5).map(topic => `
                    <div class="trending-item" onclick="window.location.href='/?type=${encodeURIComponent(topic.name)}'">
                        <div class="trending-topic">#${topic.name}</div>
                        <div class="trending-count">${topic.count} publicaciones</div>
                    </div>
                `).join('');
            } else {
                container.innerHTML = '<p class="text-muted text-center">No hay tendencias aún</p>';
            }
        })
        .catch(error => {
            console.error('Error cargando tendencias:', error);
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
    fetch(`/follow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.textContent = 'Siguiendo';
            button.classList.remove('btn-follow');
            button.classList.add('btn-following');
            button.onclick = () => unfollowUser(userId, button);
        }
    })
    .catch(error => {
        console.error('Error siguiendo usuario:', error);
    });
}

function unfollowUser(userId, button) {
    fetch(`/unfollow/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            button.textContent = 'Seguir';
            button.classList.remove('btn-following');
            button.classList.add('btn-follow');
            button.onclick = () => followUser(userId, button);
        }
    })
    .catch(error => {
        console.error('Error dejando de seguir:', error);
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
