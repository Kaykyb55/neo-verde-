/**
 * CURSOR SIMPLES - APENAS FOLHA
 * JavaScript minimalista para cursor
 */

// Verificar se é dispositivo móvel
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

if (!isMobile) {
    // Criar cursor - apenas a folha
    const cursor = document.createElement('div');
    cursor.className = 'custom-cursor';
    document.body.appendChild(cursor);

    // Atualizar posição do mouse
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    // Esconder cursor ao sair da janela
    document.addEventListener('mouseleave', () => {
        cursor.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
        cursor.style.opacity = '1';
    });

    console.log('✅ Cursor folha ativado! 🍃');
} else {
    console.log('📱 Cursor desabilitado em mobile');
}
