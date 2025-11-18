// ===== MODERN MAIN JS =====

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização
    initNavigation();
    loadDashboardStats();
    loadProjects();
    loadGallery();
    initContactForm();
    initModal();
    initScrollAnimations();
    initAnimatedElements();
    
    // Carrega os cards de destaque e conteúdo recente
    if (document.querySelector('#featured-cards')) {
        loadFeaturedCards();
    }
    
    if (document.querySelector('#recent-cards')) {
        loadRecentContent();
    }
});

// Função para carregar cards de destaque
function loadFeaturedCards() {
    const featuredContainer = document.getElementById('featured-cards');
    if (!featuredContainer) return;
    
    // Limpa o container
    featuredContainer.innerHTML = '';
    
    // Carrega projetos em destaque
    fetch('/api/projects?featured=true&limit=3')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.projects && data.projects.length > 0) {
                data.projects.forEach(project => {
                    const card = createContentCard(project, 'projeto');
                    featuredContainer.appendChild(card);
                });
            } else {
                // Se não houver projetos em destaque, carrega mídias em destaque
                return loadFeaturedMedia(featuredContainer);
            }
        })
        .catch(error => {
            console.error('Erro ao carregar projetos em destaque:', error);
            loadFeaturedMedia(featuredContainer);
        });
}

// Função para carregar mídias em destaque
function loadFeaturedMedia(container) {
    return fetch('/api/media?featured=true&limit=3')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.media && data.media.length > 0) {
                data.media.forEach(media => {
                    const card = createContentCard(media, 'media');
                    container.appendChild(card);
                });
            } else {
                container.innerHTML = '<p class="empty-message">Nenhum conteúdo em destaque disponível no momento.</p>';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar mídias em destaque:', error);
            container.innerHTML = '<p class="empty-message">Erro ao carregar conteúdo em destaque.</p>';
        });
}

// Função para carregar conteúdo recente
function loadRecentContent() {
    const recentContainer = document.getElementById('recent-cards');
    if (!recentContainer) return;
    
    // Limpa o container
    recentContainer.innerHTML = '';
    
    // Carrega projetos e mídias recentes
    Promise.all([
        fetch('/api/projects?limit=2&sort=date_desc').then(res => res.json()),
        fetch('/api/media?limit=2&sort=date_desc').then(res => res.json())
    ])
    .then(([projectsData, mediaData]) => {
        const allContent = [];
        
        if (projectsData.success && projectsData.projects) {
            projectsData.projects.forEach(project => {
                allContent.push({
                    data: project,
                    type: 'projeto',
                    date: new Date(project.created_at || project.date)
                });
            });
        }
        
        if (mediaData.success && mediaData.media) {
            mediaData.media.forEach(media => {
                allContent.push({
                    data: media,
                    type: 'media',
                    date: new Date(media.created_at || media.date)
                });
            });
        }
        
        // Ordena por data mais recente
        allContent.sort((a, b) => b.date - a.date);
        
        // Limita a 4 itens
        const recentItems = allContent.slice(0, 4);
        
        if (recentItems.length > 0) {
            recentItems.forEach(item => {
                const card = createContentCard(item.data, item.type);
                recentContainer.appendChild(card);
            });
        } else {
            recentContainer.innerHTML = '<p class="empty-message">Nenhum conteúdo recente disponível.</p>';
        }
    })
    .catch(error => {
        console.error('Erro ao carregar conteúdo recente:', error);
        recentContainer.innerHTML = '<p class="empty-message">Erro ao carregar conteúdo recente.</p>';
    });
}

// Função para criar um card de conteúdo
function createContentCard(item, type) {
    const card = document.createElement('div');
    card.className = 'content-card';
    
    // Determina a imagem e o tipo de badge
    let imageSrc = '';
    let badgeText = '';
    
    if (type === 'projeto') {
        imageSrc = item.cover_image || '/static/img/default-project.jpg';
        badgeText = 'Projeto';
    } else {
        if (item.type === 'video') {
            imageSrc = item.thumbnail || '/static/img/default-video.jpg';
            badgeText = 'Vídeo';
        } else {
            imageSrc = item.url || '/static/img/default-image.jpg';
            badgeText = 'Imagem';
        }
    }
    
    // Formata a data
    const itemDate = new Date(item.created_at || item.date || Date.now());
    const formattedDate = `${itemDate.getDate().toString().padStart(2, '0')}/${(itemDate.getMonth() + 1).toString().padStart(2, '0')}/${itemDate.getFullYear()}`;
    
    // Constrói o HTML do card
    card.innerHTML = `
        <div class="card-image-container">
            <img src="${imageSrc}" alt="${item.title || 'Conteúdo'}" class="card-image">
            <div class="card-overlay"></div>
            <span class="card-badge">${badgeText}</span>
        </div>
        <div class="card-content">
            <h3 class="card-title">${item.title || 'Sem título'}</h3>
            <p class="card-description">${item.description || 'Sem descrição disponível.'}</p>
            <div class="card-meta">
                <div class="card-stats">
                    <span class="card-stat"><i class="fas fa-heart"></i> ${item.likes_count || 0}</span>
                    <span class="card-stat"><i class="fas fa-comment"></i> ${item.comments_count || 0}</span>
                    <span class="card-stat"><i class="fas fa-eye"></i> ${item.views_count || 0}</span>
                </div>
                <span class="card-date">${formattedDate}</span>
            </div>
        </div>
    `;
    
    // Adiciona evento de clique para abrir o item
    card.addEventListener('click', () => {
        if (type === 'projeto') {
            window.location.href = `/projeto/${item.id}`;
        } else {
            openGalleryModal(item.id);
        }
    });
    
    return card;
}

// ===== ANIMAÇÕES =====
function initScrollAnimations() {
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
    
    function checkReveal() {
        const windowHeight = window.innerHeight;
        const revealPoint = 150;
        
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            if (elementTop < windowHeight - revealPoint) {
                element.classList.add('active');
            }
        });
    }
    
    // Verificar na carga inicial
    checkReveal();
    
    // Verificar no scroll
    window.addEventListener('scroll', checkReveal);
}

function initAnimatedElements() {
    // Adicionar classes de animação com delays para criar efeito sequencial
    const heroElements = document.querySelectorAll('.hero-content > *');
    heroElements.forEach((el, index) => {
        el.classList.add('fade-in');
        el.style.animationDelay = `${index * 0.2}s`;
    });
    
    // Animar cards de projetos
    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach((card, index) => {
        card.classList.add('card-enhanced');
        card.classList.add('reveal');
    });
    
    // Animar cards da galeria
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach((item, index) => {
        item.classList.add('card-enhanced');
        item.classList.add('reveal');
        if (index % 2 === 0) {
            item.classList.add('reveal-left');
        } else {
            item.classList.add('reveal-right');
        }
    });
    
    // Animar botões
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    buttons.forEach(btn => {
        btn.classList.add('btn-enhanced');
        btn.classList.add('hover-lift');
    });
}

// ===== NAVEGAÇÃO =====
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active de todos
            navItems.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));
            
            // Adiciona active no clicado
            this.classList.add('active');
            const sectionId = this.getAttribute('data-section');
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

// ===== DASHBOARD STATS =====
function loadDashboardStats() {
    // Buscar projetos
    fetch('/api/projects')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar projetos');
            }
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Resposta não é JSON válido');
            }
            return response.json();
        })
        .then(projects => {
            const activeProjectsEl = document.getElementById('active-projects-count');
            if (activeProjectsEl) activeProjectsEl.textContent = projects.length;
            
            // Mostrar projetos recentes
            displayRecentProjects(projects.slice(0, 3));
            
            // Buscar galeria
            return fetch('/api/media');
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar galeria');
            }
            const galleryContentType = response.headers.get('content-type');
            if (!galleryContentType || !galleryContentType.includes('application/json')) {
                throw new Error('Resposta da galeria não é JSON válido');
            }
            return response.json();
        })
        .then(gallery => {
            const galleryCountEl = document.getElementById('gallery-count');
            if (galleryCountEl) galleryCountEl.textContent = gallery.length;
            
            // Calcular total de curtidas
            const totalLikes = gallery.reduce((sum, item) => sum + (item.likes_count || 0), 0);
            const likesCountEl = document.getElementById('likes-count');
            if (likesCountEl) likesCountEl.textContent = totalLikes;
            
            // Calcular total de comentários
            let totalComments = 0;
            for (const item of gallery) {
                totalComments += item.comments_count || 0;
            }
            const commentsCountEl = document.getElementById('comments-count');
            if (commentsCountEl) commentsCountEl.textContent = totalComments;
            
            // Buscar usuários
            return fetch('/api/stats/users');
        })
        .then(response => response.json())
        .then(usersData => {
            const usersCountEl = document.getElementById('active-users-count');
            if (usersCountEl) usersCountEl.textContent = usersData.total;
            
            // Atualizar outros cards
            const viewsCountEl = document.getElementById('views-count');
            if (viewsCountEl) viewsCountEl.textContent = '1,234';
        })
        .catch(error => {
            console.error('Erro ao carregar estatísticas:', error);
        });
}

function displayRecentProjects(projects) {
    const container = document.getElementById('recent-projects');
    
    if (projects.length === 0) {
        container.innerHTML = '<p class="loading">Nenhum projeto encontrado</p>';
        return;
    }
    
    container.innerHTML = projects.map(project => `
        <div class="mini-card">
            <h4>${project.title}</h4>
            <p>${project.category || 'Geral'}</p>
        </div>
    `).join('');
}

// ===== PROJETOS =====
function loadProjects() {
    const container = document.getElementById('projects-container');
    if (!container) {
        console.warn('Container de projetos não encontrado');
        return;
    }
    
    container.innerHTML = '<p class="loading">Carregando projetos...</p>';
    
    console.log('Iniciando carregamento de projetos...');
    fetch('/api/projects')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na resposta da API: ${response.status} ${response.statusText}`);
            }
            
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Resposta não é JSON: ${contentType}`);
            }
            
            return response.json();
        })
        .then(data => {
            console.log('Resposta da API:', data);
            
            // Se houver erro no servidor, mostrar mensagem amigável
            if (data.error) {
                console.error('Erro do servidor:', data.error);
                container.innerHTML = '<p class="loading">Erro ao conectar com o banco de dados. Verifique se o servidor está rodando.</p>';
                return;
            }
            
            const projects = Array.isArray(data) ? data : data.projects || [];
            console.log('Projetos carregados:', projects);
            
            if (projects.length === 0) {
                container.innerHTML = '<p class="loading">Nenhum projeto disponível no momento</p>';
                return;
            }
            
            container.innerHTML = projects.map(project => `
                <div class="project-card" data-project-id="${project.id}">
                    ${project.image_url ? 
                        `<img src="${project.image_url}" alt="${project.title}" class="project-image">` : 
                        `<img src="https://via.placeholder.com/400x240/00c853/ffffff?text=Projeto+Sustent%C3%A1vel" alt="${project.title}" class="project-image">`
                    }
                    <div class="project-content">
                        <span class="project-category">${project.category || 'Sustentabilidade'}</span>
                        <h3 class="project-title">${project.title}</h3>
                        <p class="project-description">${project.description}</p>
                        <div class="project-meta">
                            <div class="project-stats">
                                <span class="stat-item">
                                    <i class="fas fa-heart"></i>
                                    <span>${project.likes_count || 0}</span>
                                </span>
                                <span class="stat-item">
                                    <i class="fas fa-comment"></i>
                                    <span>${project.comments_count || 0}</span>
                                </span>
                            </div>
                            <span class="project-date">
                                <i class="fas fa-calendar-alt"></i>
                                ${new Date(project.created_at).toLocaleDateString('pt-BR')}
                            </span>
                        </div>
                    </div>
                </div>
            `).join('');
            
            // Adicionar eventos de clique aos cards
            document.querySelectorAll('.project-card').forEach(card => {
                card.addEventListener('click', function() {
                    openProjectModal(this.dataset.projectId);
                });
            });
        })
        .catch(error => {
            console.error('Erro ao carregar projetos:', error);
            container.innerHTML = `<p class="loading">Erro ao carregar projetos: ${error.message}</p>`;
        });
}

// ===== GALERIA =====
let currentMediaId = null;

function loadGallery() {
    const container = document.getElementById('gallery-container');
    
    fetch('/api/media')
        .then(response => response.json())
        .then(gallery => {
            if (gallery.length === 0) {
                container.innerHTML = '<p class="loading">Nenhuma foto na galeria</p>';
                return;
            }
            
            container.innerHTML = gallery.map(item => {
                // Determinar se é vídeo ou imagem
                const isVideo = item.filetype && item.filetype.startsWith('video');
                const mediaHTML = isVideo 
                    ? `<video src="${item.url}" class="gallery-image" controls playsinline></video>`
                    : `<img src="${item.url}" alt="${item.filename}" class="gallery-image">`;
                
                return `
                    <div class="gallery-card" data-id="${item.id}">
                        <div class="gallery-image-container">
                            ${mediaHTML}
                            <div class="gallery-overlay"></div>
                        </div>
                        <div class="gallery-info">
                            <h4 class="gallery-title">${item.title || item.description || item.filename}</h4>
                            <p class="gallery-description">${item.category || 'Sustentabilidade'}</p>
                            <div class="gallery-stats">
                                <button class="gallery-stat likes like-btn" data-id="${item.id}">
                                    <i class="far fa-heart"></i>
                                    <span>${item.likes_count || 0}</span>
                                </button>
                                <div class="gallery-stat comments">
                                    <i class="fas fa-comment"></i>
                                    <span>${item.comments_count || 0}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
            
            // Adicionar eventos
            document.querySelectorAll('.gallery-card').forEach(card => {
                card.addEventListener('click', function(e) {
                    if (!e.target.closest('.like-btn')) {
                        openGalleryModal(this.dataset.id);
                    }
                });
            });
            
            // Eventos de curtir
            document.querySelectorAll('.like-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    toggleLike(this.dataset.id);
                });
            });
            
            // Verificar curtidas do usuário
            gallery.forEach(item => checkIfLiked(item.id));
        })
        .catch(error => {
            console.error('Erro ao carregar galeria:', error);
            container.innerHTML = '<p class="loading">Erro ao carregar galeria</p>';
        });
}

function getUserId() {
    // Função auxiliar para obter ID do usuário (pode ser implementada com session storage ou cookies)
    return sessionStorage.getItem('userId') || localStorage.getItem('userId') || null;
}

function checkIfLiked(mediaId) {
    fetch(`/api/media/${mediaId}/liked`)
        .then(response => response.json())
        .then(data => {
            const likeBtn = document.querySelector(`.like-btn[data-id="${mediaId}"]`);
            if (!likeBtn) return;
            
            if (data.liked) {
                likeBtn.classList.add('liked');
                likeBtn.querySelector('i').classList.remove('far');
                likeBtn.querySelector('i').classList.add('fas');
            }
        })
        .catch(error => {
            console.error('Erro ao verificar curtida:', error);
        });
}

function toggleLike(mediaId) {
    fetch(`/api/media/${mediaId}/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        const btn = document.querySelector(`.like-btn[data-id="${mediaId}"]`);
        
        if (btn) {
            btn.querySelector('span').textContent = data.likes_count;
            
            if (data.liked) {
                btn.classList.add('liked');
                btn.querySelector('i').classList.remove('far');
                btn.querySelector('i').classList.add('fas');
            } else {
                btn.classList.remove('liked');
                btn.querySelector('i').classList.remove('fas');
                btn.querySelector('i').classList.add('far');
            }
        }
        
        // Atualizar no modal se estiver aberto
        if (currentMediaId === mediaId) {
            document.getElementById('likes-count-modal').textContent = data.likes_count;
            const modalBtn = document.getElementById('like-btn');
            if (data.liked) {
                modalBtn.classList.add('liked');
                modalBtn.querySelector('i').classList.remove('far');
                modalBtn.querySelector('i').classList.add('fas');
            } else {
                modalBtn.classList.remove('liked');
                modalBtn.querySelector('i').classList.remove('fas');
                modalBtn.querySelector('i').classList.add('far');
            }
        }
    })
    .catch(error => {
        console.error('Erro ao curtir:', error);
    });
}

// ===== MODAL DA GALERIA =====
function initModal() {
    const modal = document.getElementById('gallery-modal');
    const closeBtn = document.querySelector('.modal-close');
    
    closeBtn.addEventListener('click', () => {
        modal.classList.remove('active');
        currentMediaId = null;
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            currentMediaId = null;
        }
    });
    
    // Form de comentário
    document.getElementById('comment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        addComment();
    });
    
    // Botão de curtir no modal
    document.getElementById('like-btn').addEventListener('click', function() {
        if (currentMediaId) {
            toggleLike(currentMediaId);
        }
    });
}

function openGalleryModal(mediaId) {
    currentMediaId = mediaId;
    const modal = document.getElementById('gallery-modal');
    
    // Buscar dados da mídia
    fetch('/api/media')
        .then(response => response.json())
        .then(allMedia => {
            const media = allMedia.find(m => m.id === mediaId);
            
            if (!media) return;
            
            // Determinar se é vídeo ou imagem
            const isVideo = media.filetype && media.filetype.startsWith('video');
            const mediaContainer = document.getElementById('modal-media-container');
            
            // Renderizar mídia correta (img ou video)
            if (isVideo) {
                mediaContainer.innerHTML = `<video id="modal-video" src="${media.url}" controls playsinline style="max-width:100%; border-radius:10px;"></video>`;
            } else {
                mediaContainer.innerHTML = `<img id="modal-img" src="${media.url}" alt="${media.filename}" style="max-width:100%; border-radius:10px;">`;
            }
            
            // Preencher informações
            document.getElementById('modal-title').textContent = media.title || media.filename;
            document.getElementById('modal-description').textContent = media.description || 'Sem descrição';
            document.getElementById('likes-count-modal').textContent = media.likes_count || 0;
            
            // Verificar se já curtiu
            return fetch(`/api/media/${mediaId}/liked`);
        })
        .then(response => response.json())
        .then(likedData => {
            const likeBtn = document.getElementById('like-btn');
            
            if (likedData.liked) {
                likeBtn.classList.add('liked');
                likeBtn.querySelector('i').classList.remove('far');
                likeBtn.querySelector('i').classList.add('fas');
            } else {
                likeBtn.classList.remove('liked');
                likeBtn.querySelector('i').classList.remove('fas');
                likeBtn.querySelector('i').classList.add('far');
            }
            
            // Carregar comentários
            loadComments(mediaId);
            
            modal.classList.add('active');
        })
        .catch(error => {
            console.error('Erro ao abrir modal:', error);
        });
}

// Função para carregar comentários de uma mídia
function loadComments(mediaId) {
    const commentsList = document.getElementById('comments-list');
    commentsList.innerHTML = '<div class="loading">Carregando comentários...</div>';
    
    fetch(`/api/media/${mediaId}/comments`)
        .then(response => response.json())
        .then(comments => {
            if (comments.length === 0) {
                commentsList.innerHTML = '<p class="no-comments">Nenhum comentário ainda. Seja o primeiro a comentar!</p>';
                return;
            }
            
            commentsList.innerHTML = comments.map(comment => `
                <div class="comment-item">
                    <div class="comment-header">
                        <strong class="comment-author">${comment.user_name}</strong>
                        <span class="comment-date">${formatDate(new Date(comment.created_at))}</span>
                    </div>
                    <p class="comment-text">${comment.text}</p>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Erro ao carregar comentários:', error);
            commentsList.innerHTML = '<p class="error">Erro ao carregar comentários</p>';
        });
}

// Função para adicionar um comentário
function addComment() {
    if (!currentMediaId) return;
    
    const nameInput = document.getElementById('comment-name');
    const textInput = document.getElementById('comment-text');
    const emailInput = document.getElementById('comment-email') || { value: '' }; // Campo opcional
    
    const name = nameInput.value.trim();
    const text = textInput.value.trim();
    const email = emailInput.value.trim();
    
    if (!name || !text) {
        alert('Por favor, preencha seu nome e comentário.');
        return;
    }
    
    fetch(`/api/media/${currentMediaId}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_name: name,
            user_email: email,
            text: text
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao enviar comentário');
        }
        return response.json();
    })
    .then(() => {
        // Limpar campos
        nameInput.value = '';
        textInput.value = '';
        if (emailInput.value) emailInput.value = '';
        
        // Recarregar comentários
        loadComments(currentMediaId);
        
        // Atualizar contador de comentários no card da galeria
        return fetch('/api/media');
    })
    .then(response => response.json())
    .then(allMedia => {
        const media = allMedia.find(m => m.id === currentMediaId);
        
        if (media) {
            const commentCountEl = document.querySelector(`.gallery-card[data-id="${currentMediaId}"] .comments span`);
            if (commentCountEl) {
                commentCountEl.textContent = media.comments_count;
            }
        }
    })
    .catch(error => {
        console.error('Erro ao adicionar comentário:', error);
        alert('Não foi possível enviar seu comentário. Tente novamente.');
    });
}

// Função auxiliar para formatar data
function formatDate(date) {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' };
    return date.toLocaleDateString('pt-BR', options);
}


// ===== FORMULÁRIO DE CONTATO =====
function initContactForm() {
    const form = document.getElementById('contact-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('contact-email').value;
            const message = document.getElementById('contact-message').value;
            const name = document.getElementById('contact-name')?.value || '';
            
            if (!email || !message) {
                alert('Por favor, preencha todos os campos obrigatórios.');
                return;
            }
            
            const submitBtn = document.getElementById('contact-submit');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Enviando...';
            }
            
            fetch('/api/contact', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
                    form.reset();
                } else {
                    alert('Erro ao enviar mensagem: ' + (data.error || 'Tente novamente.'));
                }
            })
            .catch(error => {
                console.error('Erro ao enviar mensagem:', error);
                alert('Erro ao enviar mensagem. Tente novamente.');
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Enviar Mensagem';
                }
            });
        });
    }
}

// ===== BUSCA =====
document.querySelector('.search-bar input').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    // Buscar em projetos
    document.querySelectorAll('.project-card').forEach(card => {
        const title = card.querySelector('.project-title')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.project-description')?.textContent.toLowerCase() || '';
        
        if (title.includes(searchTerm) || description.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
    
    // Buscar na galeria
    document.querySelectorAll('.gallery-card').forEach(card => {
        const img = card.querySelector('img');
        const alt = img?.alt.toLowerCase() || '';
        
        if (alt.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// ===== PROJECT MODAL FUNCTIONS =====
let currentProjectId = null;

function openProjectModal(projectId) {
    currentProjectId = projectId;
    
    // Criar modal dinamicamente se não existir
    let modal = document.getElementById('project-modal');
    if (!modal) {
        modal = createProjectModal();
        document.body.appendChild(modal);
    }
    
    // Buscar dados do projeto
    fetch('/api/projects')
        .then(response => response.json())
        .then(allProjects => {
            const project = allProjects.find(p => p.id === projectId);
            
            if (!project) return;
            
            // Preencher modal
            document.getElementById('project-modal-img').src = project.image_url || 'https://via.placeholder.com/600x400/00c853/ffffff?text=Projeto';
            document.getElementById('project-modal-title').textContent = project.title;
            document.getElementById('project-modal-description').textContent = project.description;
            document.getElementById('project-modal-category').textContent = project.category || 'Sustentabilidade';
            document.getElementById('project-likes-count-modal').textContent = project.likes_count || 0;
            
            // Carregar comentários
            loadProjectComments(projectId);
            
            modal.classList.add('active');
        })
        .catch(error => {
            console.error('Erro ao abrir modal de projeto:', error);
        });
}

function createProjectModal() {
    const modal = document.createElement('div');
    modal.id = 'project-modal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="modal-close" id="project-modal-close">&times;</span>
            <div class="modal-body">
                <div class="modal-image">
                    <img id="project-modal-img" src="" alt="">
                </div>
                <div class="modal-info">
                    <span class="project-category" id="project-modal-category"></span>
                    <h3 id="project-modal-title"></h3>
                    <p id="project-modal-description"></p>
                    
                    <div class="modal-actions">
                        <button id="project-like-btn" class="action-btn">
                            <i class="far fa-heart"></i>
                            <span id="project-likes-count-modal">0</span>
                        </button>
                    </div>
                    
                    <div class="comments-section">
                        <h4>Comentários</h4>
                        <div id="project-comments-list"></div>
                        
                        <form id="project-comment-form" class="comment-form">
                            <input type="text" id="project-comment-name" placeholder="Seu nome" required>
                            <textarea id="project-comment-text" placeholder="Seu comentário..." required></textarea>
                            <button type="submit">Comentar</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Adicionar eventos
    modal.querySelector('#project-modal-close').addEventListener('click', () => {
        modal.classList.remove('active');
        currentProjectId = null;
    });
    
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.classList.remove('active');
            currentProjectId = null;
        }
    });
    
    modal.querySelector('#project-comment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        addProjectComment();
    });
    
    modal.querySelector('#project-like-btn').addEventListener('click', function() {
        if (currentProjectId) {
            toggleProjectLike(currentProjectId);
        }
    });
    
    return modal;
}

function loadProjectComments(projectId) {
    const commentsList = document.getElementById('project-comments-list');
    if (!commentsList) return;
    
    commentsList.innerHTML = '<div class="loading">Carregando comentários...</div>';
    
    fetch(`/api/projects/${projectId}/comments`)
        .then(response => response.json())
        .then(comments => {
            if (comments.length === 0) {
                commentsList.innerHTML = '<p class="no-comments">Nenhum comentário ainda. Seja o primeiro a comentar!</p>';
                return;
            }
            
            commentsList.innerHTML = comments.map(comment => `
                <div class="comment-item">
                    <div class="comment-header">
                        <strong class="comment-author">${comment.user_name}</strong>
                        <span class="comment-date">${formatDate(new Date(comment.created_at))}</span>
                    </div>
                    <p class="comment-text">${comment.text}</p>
                </div>
            `).join('');
        })
        .catch(error => {
            console.error('Erro ao carregar comentários do projeto:', error);
            commentsList.innerHTML = '<p class="error">Erro ao carregar comentários</p>';
        });
}

function addProjectComment() {
    if (!currentProjectId) return;
    
    const nameInput = document.getElementById('project-comment-name');
    const textInput = document.getElementById('project-comment-text');
    
    if (!nameInput || !textInput) return;
    
    const name = nameInput.value.trim();
    const text = textInput.value.trim();
    
    if (!name || !text) {
        alert('Por favor, preencha seu nome e comentário.');
        return;
    }
    
    fetch(`/api/projects/${currentProjectId}/comment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_name: name,
            text: text
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao enviar comentário');
        }
        return response.json();
    })
    .then(() => {
        // Limpar campos
        nameInput.value = '';
        textInput.value = '';
        
        // Recarregar comentários
        loadProjectComments(currentProjectId);
        
        // Atualizar contador de comentários no card do projeto
        loadProjects();
    })
    .catch(error => {
        console.error('Erro ao adicionar comentário ao projeto:', error);
        alert('Não foi possível enviar seu comentário. Tente novamente.');
    });
}

function toggleProjectLike(projectId) {
    fetch(`/api/projects/${projectId}/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const likesEl = document.getElementById('project-likes-count-modal');
            if (likesEl) {
                likesEl.textContent = data.likes_count;
            }
            
            const likeBtn = document.getElementById('project-like-btn');
            if (likeBtn) {
                likeBtn.classList.add('liked');
                const icon = likeBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                }
            }
            
            // Atualizar card do projeto
            loadProjects();
        }
    })
    .catch(error => {
        console.error('Erro ao curtir projeto:', error);
    });
}
