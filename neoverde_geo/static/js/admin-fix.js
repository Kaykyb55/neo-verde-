/**
 * Admin JavaScript - Versão Simplificada e Funcionando
 */

console.log('✅ Admin JS carregado!');

// Carregar quando a página estiver pronta
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOM carregado!');
    
    // Carregar dashboard imediatamente
    carregarDashboard();
    
    // Setup navegação
    setupNavegacao();
    
    // Setup modais e botões
    setupModais();
    setupUpload();
    setupBotoes();
    
    // Inicializar câmera
    let cameraStream = null;
    let capturedPhotoFile = null;

    // Botão de abrir câmera
    const openCameraBtn = document.getElementById('open-camera-btn');
    if (openCameraBtn) {
        openCameraBtn.addEventListener('click', async function() {
            console.log('📷 Abrindo câmera...');
            const cameraContainer = document.getElementById('camera-container');
            const video = document.getElementById('camera-video');
            
            try {
                // Solicitar acesso à câmera
                cameraStream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' }, // usar câmera traseira se disponível
                    audio: false 
                });
                
                video.srcObject = cameraStream;
                cameraContainer.style.display = 'block';
                openCameraBtn.style.display = 'none';
                
                console.log('✅ Câmera aberta!');
            } catch (error) {
                console.error('❌ Erro ao acessar câmera:', error);
                alert('❌ Erro ao acessar câmera. Verifique as permissões!');
            }
        });
    }

    // Botão de capturar foto
    const capturePhotoBtn = document.getElementById('capture-photo-btn');
    if (capturePhotoBtn) {
        capturePhotoBtn.addEventListener('click', function() {
            console.log('📸 Capturando foto...');
            const video = document.getElementById('camera-video');
            const canvas = document.getElementById('photo-canvas');
            const preview = document.getElementById('media-preview');
            
            // Configurar canvas com o tamanho do vídeo
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            
            // Desenhar frame atual do vídeo no canvas
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Converter canvas para blob e então para File
            canvas.toBlob(function(blob) {
                const filename = `camera_${Date.now()}.jpg`;
                capturedPhotoFile = new File([blob], filename, { type: 'image/jpeg' });
                
                // Mostrar preview
                const imgUrl = URL.createObjectURL(blob);
                preview.innerHTML = `<img src="${imgUrl}" style="max-width: 100%; border-radius: 10px;">`;
                
                // Parar câmera
                if (cameraStream) {
                    cameraStream.getTracks().forEach(track => track.stop());
                    cameraStream = null;
                }
                
                document.getElementById('camera-container').style.display = 'none';
                document.getElementById('open-camera-btn').style.display = 'block';
                
                console.log('✅ Foto capturada!');
                alert('✅ Foto capturada! Agora preencha os campos e clique em Salvar.');
            }, 'image/jpeg', 0.95);
        });
    }

    // Botão de fechar câmera
    const closeCameraBtn = document.getElementById('close-camera-btn');
    if (closeCameraBtn) {
        closeCameraBtn.addEventListener('click', function() {
            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
                cameraStream = null;
            }
            
            document.getElementById('camera-container').style.display = 'none';
            document.getElementById('open-camera-btn').style.display = 'block';
            
            console.log('📷 Câmera fechada');
        });
    }

    // Atualizar o formulário de mídia para usar foto capturada se existir
    const mediaFormOriginal = document.getElementById('media-form');
    if (mediaFormOriginal) {
        mediaFormOriginal.addEventListener('submit', async function(e) {
            const mediaFileInput = document.getElementById('media-file');
            
            // Se tem foto capturada e não tem arquivo selecionado, usar a foto
            if (capturedPhotoFile && !mediaFileInput.files.length) {
                // Criar um DataTransfer para simular seleção de arquivo
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(capturedPhotoFile);
                mediaFileInput.files = dataTransfer.files;
                
                console.log('📸 Usando foto capturada pela câmera');
            }
            
            // Limpar foto capturada após uso
            capturedPhotoFile = null;
        });
    }
});

// ==================================================
// DASHBOARD
// ==================================================

function carregarDashboard() {
    console.log('📊 Carregando dashboard...');
    
    // Carregar projetos
    fetch('/api/projects')
        .then(response => {
            console.log('Resposta /api/projects:', response.status);
            return response.json();
        })
        .then(projects => {
            console.log(`✅ ${projects.length} projetos carregados:`, projects);
            document.getElementById('admin-projects-count').textContent = projects.length || 0;
            
            // Contar curtidas dos projetos
            let totalLikes = 0;
            projects.forEach(p => totalLikes += (p.likes_count || 0));
            document.getElementById('admin-likes-count').textContent = totalLikes;
            
            // Contar comentários dos projetos
            let totalComments = 0;
            projects.forEach(p => totalComments += (p.comments_count || 0));
            
            return fetch('/api/media');
        })
        .then(response => {
            console.log('Resposta /api/media:', response.status);
            return response.json();
        })
        .then(media => {
            console.log(`✅ ${media.length} fotos carregadas:`, media);
            document.getElementById('admin-media-count').textContent = media.length || 0;
            
            // Atualizar comentários e curtidas totais
            let totalComments = 0;
            let totalLikes = 0;
            media.forEach(m => {
                totalComments += (m.comments_count || 0);
                totalLikes += (m.likes_count || 0);
            });
            
            const likesElement = document.getElementById('admin-likes-count');
            const commentsElement = document.getElementById('admin-comments-count');
            
            if (likesElement) {
                const currentLikes = parseInt(likesElement.textContent) || 0;
                likesElement.textContent = currentLikes + totalLikes;
            }
            
            if (commentsElement) {
                commentsElement.textContent = totalComments;
            }
            
            return fetch('/api/contact/messages');
        })
        .then(response => response.json())
        .then(messages => {
            console.log(`✅ ${messages.length} mensagens carregadas`);
            document.getElementById('admin-messages-count').textContent = messages.length || 0;
            
            const unread = messages.filter(m => !m.read).length;
            const unreadElement = document.getElementById('admin-unread-messages');
            if (unreadElement) {
                unreadElement.textContent = unread;
            }
            
            console.log('✅ Dashboard carregado com sucesso!');
        })
        .catch(error => {
            console.error('❌ Erro ao carregar dashboard:', error);
            // Pelo menos mostrar zero em vez de erro
            document.getElementById('admin-projects-count').textContent = '0';
            document.getElementById('admin-media-count').textContent = '0';
            document.getElementById('admin-messages-count').textContent = '0';
        });
}

// ==================================================
// NAVEGAÇÃO
// ==================================================

function setupNavegacao() {
    console.log('🔗 Configurando navegação...');
    
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover active de todos
            navItems.forEach(nav => nav.classList.remove('active'));
            document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
            
            // Adicionar active no clicado
            this.classList.add('active');
            
            const sectionId = this.dataset.section;
            const section = document.getElementById(sectionId);
            
            if (section) {
                section.classList.add('active');
                console.log(`📄 Seção ativa: ${sectionId}`);
                
                // Carregar dados da seção
                carregarSecao(sectionId);
            }
        });
    });
    
    console.log('✅ Navegação configurada!');
}

function carregarSecao(sectionId) {
    console.log(`📥 Carregando seção: ${sectionId}`);
    
    switch(sectionId) {
        case 'dashboard-admin':
            carregarDashboard();
            break;
        case 'projetos-admin':
            carregarProjetos();
            break;
        case 'galeria-admin':
            carregarGaleria();
            break;
        case 'mensagens-admin':
            carregarMensagens();
            break;
    }
}

// ==================================================
// PROJETOS
// ==================================================

function carregarProjetos() {
    console.log('🌱 Carregando projetos...');
    
    const container = document.getElementById('projects-admin-list');
    if (!container) {
        console.error('❌ Container projects-admin-list não encontrado!');
        return;
    }
    
    container.innerHTML = '<div class="loading">Carregando projetos...</div>';
    
    fetch('/api/projects')
        .then(response => response.json())
        .then(projects => {
            console.log(`✅ ${projects.length} projetos para exibir`);
            
            if (!projects || projects.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">Nenhum projeto cadastrado</p>';
                return;
            }
            
            container.innerHTML = projects.map(project => `
                <div class="admin-card" style="border:1px solid #ddd; border-radius:10px; overflow:hidden; background:white;">
                    <img src="${project.image_url || 'https://via.placeholder.com/300x200'}" 
                         alt="${project.title}" 
                         style="width:100%; height:200px; object-fit:cover;">
                    <div style="padding:15px;">
                        <h3 style="margin:0 0 10px 0; color:#333;">${project.title}</h3>
                        <p style="color:#666; font-size:14px;">${project.category || 'Sem categoria'}</p>
                        <div style="display:flex; gap:15px; margin:10px 0; color:#999; font-size:14px;">
                            <span>❤️ ${project.likes_count || 0}</span>
                            <span>💬 ${project.comments_count || 0}</span>
                        </div>
                        <div style="display:flex; gap:10px;">
                            <button onclick="editarProjeto('${project.id}')" 
                                    style="background:#2196F3; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">
                                ✏️ Editar
                            </button>
                            <button onclick="deletarProjeto('${project.id}')" 
                                    style="background:#f44336; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">
                                🗑️ Deletar
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
            
            console.log('✅ Projetos exibidos!');
        })
        .catch(error => {
            console.error('❌ Erro ao carregar projetos:', error);
            container.innerHTML = '<p style="text-align:center;color:red;padding:40px;">Erro ao carregar projetos</p>';
        });
}

function editarProjeto(id) {
    console.log('✏️ Editando projeto:', id);
    
    // Buscar dados do projeto
    fetch(`/api/projects`)
        .then(response => response.json())
        .then(projects => {
            const project = projects.find(p => p.id === id);
            if (!project) {
                alert('❌ Projeto não encontrado!');
                return;
            }
            
            // Preencher modal com dados do projeto
            document.getElementById('project-id').value = project.id;
            document.getElementById('project-title').value = project.title;
            document.getElementById('project-description').value = project.description;
            document.getElementById('project-category').value = project.category || 'sustentabilidade';
            document.getElementById('project-image').value = project.image_url || '';
            
            // Mostrar preview da imagem atual
            if (project.image_url) {
                document.getElementById('project-image-preview').innerHTML = 
                    `<img src="${project.image_url}" style="max-width: 100%; border-radius: 10px;">`;
            }
            
            // Mudar título do modal
            document.getElementById('project-modal-title').textContent = 'Editar Projeto';
            
            // Mostrar modal
            document.getElementById('project-modal').style.display = 'flex';
        })
        .catch(error => {
            console.error('Erro ao buscar projeto:', error);
            alert('❌ Erro ao carregar dados do projeto');
        });
}

function deletarProjeto(id) {
    if (!confirm('Tem certeza que deseja deletar este projeto?')) return;
    
    fetch(`/api/projects/${id}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                alert('✅ Projeto deletado!');
                carregarProjetos();
                carregarDashboard();
            } else {
                alert('❌ Erro ao deletar projeto');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('❌ Erro ao deletar projeto');
        });
}

// ==================================================
// GALERIA
// ==================================================

function carregarGaleria() {
    console.log('🖼️ Carregando galeria...');
    
    const container = document.getElementById('gallery-admin-list');
    if (!container) {
        console.error('❌ Container gallery-admin-list não encontrado!');
        return;
    }
    
    container.innerHTML = '<div class="loading">Carregando galeria...</div>';
    
    fetch('/api/media')
        .then(response => response.json())
        .then(media => {
            console.log(`✅ ${media.length} fotos para exibir`);
            
            if (!media || media.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">Nenhuma foto cadastrada</p>';
                return;
            }
            
            container.innerHTML = media.map(item => `
                <div class="admin-card" style="border:1px solid #ddd; border-radius:10px; overflow:hidden; background:white;">
                    <img src="${item.url || 'https://via.placeholder.com/300x200'}" 
                         alt="${item.title}" 
                         style="width:100%; height:200px; object-fit:cover;">
                    <div style="padding:15px;">
                        <h3 style="margin:0 0 10px 0; color:#333;">${item.title}</h3>
                        <p style="color:#666; font-size:14px;">${item.category || 'Sem categoria'}</p>
                        <div style="display:flex; gap:15px; margin:10px 0; color:#999; font-size:14px;">
                            <span>❤️ ${item.likes_count || 0}</span>
                            <span>💬 ${item.comments_count || 0}</span>
                        </div>
                        <div style="display:flex; gap:10px;">
                            <button onclick="editarMidia('${item.id}')" 
                                    style="background:#2196F3; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">
                                ✏️ Editar
                            </button>
                            <button onclick="deletarMidia('${item.id}')" 
                                    style="background:#f44336; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer;">
                                🗑️ Deletar
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
            
            console.log('✅ Galeria exibida!');
        })
        .catch(error => {
            console.error('❌ Erro ao carregar galeria:', error);
            container.innerHTML = '<p style="text-align:center;color:red;padding:40px;">Erro ao carregar galeria</p>';
        });
}

function editarMidia(id) {
    console.log('✏️ Editando mídia:', id);
    
    // Buscar dados da mídia
    fetch(`/api/media`)
        .then(response => response.json())
        .then(mediaList => {
            const media = mediaList.find(m => m.id === id);
            if (!media) {
                alert('❌ Mídia não encontrada!');
                return;
            }
            
            // Preencher modal com dados da mídia
            document.getElementById('media-id').value = media.id;
            document.getElementById('media-title').value = media.title;
            document.getElementById('media-description').value = media.description || '';
            document.getElementById('media-category').value = media.category || 'sustentabilidade';
            
            // Mostrar preview da mídia atual
            if (media.url) {
                const preview = document.getElementById('media-preview');
                if (media.filetype && media.filetype.startsWith('video')) {
                    preview.innerHTML = `<video src="${media.url}" controls style="max-width: 100%; border-radius: 10px;"></video>`;
                } else {
                    preview.innerHTML = `<img src="${media.url}" style="max-width: 100%; border-radius: 10px;">`;
                }
            }
            
            // Mudar título do modal
            document.getElementById('media-modal-title').textContent = 'Editar Mídia';
            
            // Mostrar modal
            document.getElementById('media-modal').style.display = 'flex';
        })
        .catch(error => {
            console.error('Erro ao buscar mídia:', error);
            alert('❌ Erro ao carregar dados da mídia');
        });
}

function deletarMidia(id) {
    if (!confirm('Tem certeza que deseja deletar esta mídia?')) return;
    
    fetch(`/api/media/${id}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                alert('✅ Mídia deletada!');
                carregarGaleria();
                carregarDashboard();
            } else {
                alert('❌ Erro ao deletar mídia');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('❌ Erro ao deletar mídia');
        });
}

// ==================================================
// MENSAGENS
// ==================================================

function carregarMensagens() {
    console.log('💬 Carregando mensagens...');
    
    const container = document.getElementById('messages-list');
    if (!container) {
        console.error('❌ Container messages-list não encontrado!');
        return;
    }
    
    container.innerHTML = '<div class="loading">Carregando mensagens...</div>';
    
    fetch('/api/contact/messages')
        .then(response => response.json())
        .then(messages => {
            console.log(`✅ ${messages.length} mensagens carregadas`);
            
            if (!messages || messages.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#666;padding:40px;">Nenhuma mensagem recebida</p>';
                return;
            }
            
            container.innerHTML = messages.map(msg => `
                <div style="border:1px solid #ddd; border-radius:10px; padding:20px; margin-bottom:15px; background:white;">
                    <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;">
                        <div style="flex:1;">
                            <strong style="color:#333;">${msg.email}</strong>
                            <span style="color:#999; font-size:12px; margin-left:15px;">${new Date(msg.created_at).toLocaleDateString('pt-BR')}</span>
                        </div>
                        <button onclick="deletarMensagem('${msg.id}')" 
                                style="background:#f44336; color:white; border:none; padding:6px 12px; border-radius:5px; cursor:pointer; font-size:12px;">
                            🗑️ Deletar
                        </button>
                    </div>
                    <p style="color:#666; margin:0;">${msg.message}</p>
                </div>
            `).join('');
            
            console.log('✅ Mensagens exibidas!');
        })
        .catch(error => {
            console.error('❌ Erro ao carregar mensagens:', error);
            container.innerHTML = '<p style="text-align:center;color:red;padding:40px;">Erro ao carregar mensagens</p>';
        });
}

function deletarMensagem(id) {
    if (!confirm('Tem certeza que deseja deletar esta mensagem?')) return;
    
    fetch(`/api/contact/messages/${id}`, { method: 'DELETE' })
        .then(response => {
            if (response.ok) {
                alert('✅ Mensagem deletada!');
                carregarMensagens();
                carregarDashboard();
            } else {
                alert('❌ Erro ao deletar mensagem');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('❌ Erro ao deletar mensagem');
        });
}

// ==================================================
// MODAIS
// ==================================================

function setupModais() {
    console.log('🔧 Configurando modais...');
    
    // Fechar modais ao clicar no X ou fora
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        // Fechar ao clicar no X
        const closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
        
        // Fechar ao clicar fora
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
        
        // Fechar ao clicar no botão cancelar
        const cancelBtn = modal.querySelector('.modal-close-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
    });
    
    console.log('✅ Modais configurados!');
}

// ==================================================
// BOTÕES
// ==================================================

function setupBotoes() {
    console.log('🔧 Configurando botões...');
    
    // Botão Novo Projeto
    const addProjectBtn = document.getElementById('add-project-btn');
    if (addProjectBtn) {
        addProjectBtn.addEventListener('click', () => {
            console.log('➕ Abrindo modal de novo projeto...');
            abrirModalProjeto();
        });
    }
    
    // Botão Nova Mídia
    const addMediaBtn = document.getElementById('add-media-btn');
    if (addMediaBtn) {
        addMediaBtn.addEventListener('click', () => {
            console.log('➕ Abrindo modal de nova mídia...');
            abrirModalMidia();
        });
    }
    
    // Botão Refresh
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            location.reload();
        });
    }
    
    console.log('✅ Botões configurados!');
}

// ==================================================
// MODAL PROJETO
// ==================================================

function abrirModalProjeto() {
    console.log('🚀 Abrindo modal de novo projeto...');
    const modal = document.getElementById('project-modal');
    if (!modal) {
        console.error('❌ Modal de projeto não encontrado!');
        return;
    }
    
    // Limpar formulário
    document.getElementById('project-id').value = '';
    document.getElementById('project-title').value = '';
    document.getElementById('project-description').value = '';
    document.getElementById('project-category').value = 'sustentabilidade';
    document.getElementById('project-image').value = '';
    document.getElementById('project-image-file').value = '';
    document.getElementById('project-image-preview').innerHTML = '';
    
    // Mudar título para "Novo Projeto"
    document.getElementById('project-modal-title').textContent = 'Novo Projeto';
    
    // Mostrar modal
    modal.style.display = 'flex';
    console.log('✅ Modal de projeto aberto!');
}

// Preview da imagem do projeto
const projectImageFile = document.getElementById('project-image-file');
if (projectImageFile) {
    projectImageFile.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('project-image-preview');
                preview.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; border-radius: 10px;">`;
            };
            reader.readAsDataURL(file);
        }
    });
}

// Formulário de projeto
const projectForm = document.getElementById('project-form');
if (projectForm) {
    projectForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('📤 Enviando projeto...');
        
        const projectId = document.getElementById('project-id').value;
        const title = document.getElementById('project-title').value;
        const description = document.getElementById('project-description').value;
        const category = document.getElementById('project-category').value;
        const imageFile = document.getElementById('project-image-file').files[0];
        const imageUrl = document.getElementById('project-image').value;
        
        if (!title || !description) {
            alert('❌ Preencha todos os campos obrigatórios!');
            return;
        }
        
        try {
            let response;
            const isEditing = projectId && projectId.trim() !== '';
            
            // Se está editando
            if (isEditing) {
                // Se tem novo arquivo, envia como FormData
                if (imageFile) {
                    const formData = new FormData();
                    formData.append('title', title);
                    formData.append('description', description);
                    formData.append('category', category);
                    formData.append('image', imageFile);
                    
                    response = await fetch(`/api/projects/${projectId}`, {
                        method: 'PUT',
                        body: formData
                    });
                } else {
                    // Atualiza apenas os dados
                    response = await fetch(`/api/projects/${projectId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            title: title,
                            description: description,
                            category: category,
                            image_url: imageUrl || undefined
                        })
                    });
                }
            } else {
                // Criando novo projeto
                if (imageFile) {
                    const formData = new FormData();
                    formData.append('title', title);
                    formData.append('description', description);
                    formData.append('category', category);
                    formData.append('image', imageFile);
                    
                    response = await fetch('/api/projects', {
                        method: 'POST',
                        body: formData
                    });
                } else if (imageUrl) {
                    response = await fetch('/api/projects', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            title: title,
                            description: description,
                            category: category,
                            image_url: imageUrl
                        })
                    });
                } else {
                    alert('❌ Adicione uma imagem (arquivo ou URL)!');
                    return;
                }
            }
            
            if (response.ok) {
                alert(isEditing ? '✅ Projeto atualizado com sucesso!' : '✅ Projeto criado com sucesso!');
                document.getElementById('project-modal').style.display = 'none';
                carregarProjetos();
                carregarDashboard();
            } else {
                const error = await response.json();
                alert('❌ Erro: ' + (error.error || 'Erro desconhecido'));
            }
        } catch (error) {
            console.error('❌ Erro:', error);
            alert('❌ Erro ao salvar projeto: ' + error.message);
        }
    });
}

// ==================================================
// MODAL MÍDIA
// ==================================================

function abrirModalMidia() {
    console.log('🚀 Abrindo modal de nova mídia...');
    const modal = document.getElementById('media-modal');
    if (!modal) {
        console.error('❌ Modal de mídia não encontrado!');
        return;
    }
    
    // Limpar formulário
    document.getElementById('media-id').value = '';
    document.getElementById('media-title').value = '';
    document.getElementById('media-description').value = '';
    document.getElementById('media-category').value = 'sustentabilidade';
    document.getElementById('media-file').value = '';
    document.getElementById('media-preview').innerHTML = '';
    
    // Mudar título para "Nova Mídia"
    document.getElementById('media-modal-title').textContent = 'Nova Mídia';
    
    // Mostrar modal
    modal.style.display = 'flex';
    console.log('✅ Modal de mídia aberto!');
}

// Preview da mídia
const mediaFile = document.getElementById('media-file');
if (mediaFile) {
    mediaFile.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('media-preview');
                if (file.type.startsWith('image/')) {
                    preview.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; border-radius: 10px;">`;
                } else if (file.type.startsWith('video/')) {
                    preview.innerHTML = `<video src="${event.target.result}" controls style="max-width: 100%; border-radius: 10px;"></video>`;
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

// Formulário de mídia
const mediaForm = document.getElementById('media-form');
if (mediaForm) {
    mediaForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('📤 Enviando mídia...');
        
        const mediaId = document.getElementById('media-id').value;
        const title = document.getElementById('media-title').value;
        const description = document.getElementById('media-description').value;
        const category = document.getElementById('media-category').value;
        const file = document.getElementById('media-file').files[0];
        
        const isEditing = mediaId && mediaId.trim() !== '';
        
        if (!title || !description) {
            alert('❌ Preencha todos os campos obrigatórios!');
            return;
        }
        
        if (!isEditing && !file) {
            alert('❌ Selecione um arquivo!');
            return;
        }
        
        try {
            let response;
            
            if (isEditing) {
                // Editando mídia - apenas atualiza metadados
                response = await fetch(`/api/media/${mediaId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        title: title,
                        description: description,
                        category: category
                    })
                });
            } else {
                // Criando nova mídia
                const formData = new FormData();
                formData.append('file', file);
                formData.append('title', title);
                formData.append('description', description);
                formData.append('category', category);
                
                response = await fetch('/api/media/upload', {
                    method: 'POST',
                    body: formData
                });
            }
            
            if (response.ok) {
                alert(isEditing ? '✅ Mídia atualizada com sucesso!' : '✅ Mídia enviada com sucesso!');
                document.getElementById('media-modal').style.display = 'none';
                carregarGaleria();
                carregarDashboard();
            } else {
                const error = await response.json();
                alert('❌ Erro: ' + (error.error || 'Erro desconhecido'));
            }
        } catch (error) {
            console.error('❌ Erro:', error);
            alert('❌ Erro ao salvar mídia: ' + error.message);
        }
    });
}

// ==================================================
// UPLOAD DRAG & DROP
// ==================================================

function setupUpload() {
    console.log('🔧 Configurando upload drag & drop...');
    
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadPreview = document.getElementById('upload-preview');
    
    if (!dropzone || !fileInput || !uploadBtn) {
        console.warn('⚠️ Elementos de upload não encontrados');
        return;
    }
    
    let selectedFiles = [];
    
    // Click na dropzone abre o seletor de arquivos
    dropzone.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Prevenir comportamento padrão do drag & drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Destacar dropzone quando arrastar arquivo
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.style.borderColor = '#4CAF50';
            dropzone.style.background = '#f1f8f4';
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => {
            dropzone.style.borderColor = '#ddd';
            dropzone.style.background = '#f9f9f9';
        });
    });
    
    // Gerenciar drop de arquivos
    dropzone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        handleFiles(files);
    });
    
    // Gerenciar seleção de arquivos
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        handleFiles(files);
    });
    
    function handleFiles(files) {
        selectedFiles = Array.from(files);
        console.log(`📁 ${selectedFiles.length} arquivo(s) selecionado(s)`);
        
        uploadPreview.innerHTML = '';
        
        selectedFiles.forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.createElement('div');
                preview.style.cssText = 'display: inline-block; margin: 10px; position: relative;';
                
                if (file.type.startsWith('image/')) {
                    preview.innerHTML = `
                        <img src="${e.target.result}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px;">
                        <p style="text-align: center; margin-top: 5px; font-size: 12px;">${file.name}</p>
                    `;
                } else if (file.type.startsWith('video/')) {
                    preview.innerHTML = `
                        <video src="${e.target.result}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 10px;"></video>
                        <p style="text-align: center; margin-top: 5px; font-size: 12px;">${file.name}</p>
                    `;
                }
                
                uploadPreview.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });
        
        uploadBtn.disabled = selectedFiles.length === 0;
    }
    
    // Botão de upload
    uploadBtn.addEventListener('click', async () => {
        if (selectedFiles.length === 0) {
            alert('❌ Selecione pelo menos um arquivo!');
            return;
        }
        
        const category = document.getElementById('upload-category').value;
        const description = document.getElementById('upload-description').value;
        
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
        
        let sucessos = 0;
        let erros = 0;
        
        for (const file of selectedFiles) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('category', category);
            formData.append('description', description);
            formData.append('title', file.name.split('.')[0]);
            
            try {
                const response = await fetch('/api/media/upload', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    sucessos++;
                } else {
                    erros++;
                }
            } catch (error) {
                console.error('Erro ao enviar arquivo:', error);
                erros++;
            }
        }
        
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Fazer Upload';
        
        alert(`✅ ${sucessos} arquivo(s) enviado(s) com sucesso!\n${erros > 0 ? `❌ ${erros} erro(s)` : ''}`);
        
        // Limpar
        selectedFiles = [];
        fileInput.value = '';
        uploadPreview.innerHTML = '';
        document.getElementById('upload-description').value = '';
        
        // Recarregar galeria
        carregarGaleria();
        carregarDashboard();
    });
    
    console.log('✅ Upload drag & drop configurado!');
}

console.log('✅ Admin Fix JS completamente carregado!');
