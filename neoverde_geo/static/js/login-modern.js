// ===== MODERN LOGIN JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    // Tab Switching
    const authTabs = document.querySelectorAll('.auth-tab');
    const authContents = document.querySelectorAll('.auth-content');

    authTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs
            authTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all content
            authContents.forEach(content => content.classList.remove('active'));
            
            // Show target content
            document.getElementById(`${targetTab}-content`).classList.add('active');
        });
    });

    // Password Toggle
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Login Form Validation
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;
            
            if (!email || !password) {
                e.preventDefault();
                showAlert('Por favor, preencha todos os campos!', 'error');
                return;
            }
            
            if (!validateEmail(email)) {
                e.preventDefault();
                showAlert('Por favor, insira um email válido!', 'error');
                return;
            }
        });
    }

    // Register Form Validation
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const name = document.getElementById('reg-name').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const password = document.getElementById('reg-password').value;
            const confirmPassword = document.getElementById('reg-confirm-password').value;
            const terms = document.getElementById('terms').checked;
            
            if (!name || !email || !password || !confirmPassword) {
                e.preventDefault();
                showAlert('Por favor, preencha todos os campos!', 'error');
                return;
            }
            
            if (!validateEmail(email)) {
                e.preventDefault();
                showAlert('Por favor, insira um email válido!', 'error');
                return;
            }
            
            if (password.length < 6) {
                e.preventDefault();
                showAlert('A senha deve ter pelo menos 6 caracteres!', 'error');
                return;
            }
            
            if (password !== confirmPassword) {
                e.preventDefault();
                showAlert('As senhas não coincidem!', 'error');
                return;
            }
            
            if (!terms) {
                e.preventDefault();
                showAlert('Você precisa concordar com os termos de uso!', 'error');
                return;
            }
        });
    }

    // Email Validation
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Show Alert Function
    function showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.flash-message');
        existingAlerts.forEach(alert => alert.remove());
        
        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `flash-message flash-${type}`;
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        // Insert alert before tabs
        const authTabs = document.querySelector('.auth-tabs');
        authTabs.parentNode.insertBefore(alertDiv, authTabs);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            alertDiv.style.transition = 'opacity 0.3s';
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }

    // Password Strength Indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.id === 'reg-password') {
            input.addEventListener('input', function() {
                updatePasswordStrength(this.value);
            });
        }
    });

    function updatePasswordStrength(password) {
        const hint = document.querySelector('.password-hint');
        if (!hint) return;
        
        const strength = calculatePasswordStrength(password);
        const icon = hint.querySelector('i');
        
        if (strength === 'weak') {
            hint.style.color = '#f44336';
            icon.className = 'fas fa-times-circle';
            hint.querySelector('span') ? hint.querySelector('span').textContent = 'Senha fraca' : null;
        } else if (strength === 'medium') {
            hint.style.color = '#ff9800';
            icon.className = 'fas fa-info-circle';
            hint.querySelector('span') ? hint.querySelector('span').textContent = 'Senha média' : null;
        } else if (strength === 'strong') {
            hint.style.color = '#00c853';
            icon.className = 'fas fa-check-circle';
            hint.querySelector('span') ? hint.querySelector('span').textContent = 'Senha forte!' : null;
        }
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        
        if (strength <= 2) return 'weak';
        if (strength <= 4) return 'medium';
        return 'strong';
    }

    // Social Login Buttons
    const socialButtons = document.querySelectorAll('.social-btn');
    socialButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('google')) {
                // Redirecionar para OAuth Google
                window.location.href = '/login/google';
            } else if (this.classList.contains('facebook')) {
                showAlert('Login com Facebook em desenvolvimento.', 'error');
            }
        });
    });

    // Auto-dismiss flash messages
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.3s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Add smooth transitions
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s';
        document.body.style.opacity = '1';
    }, 100);

    // Form Input Animations
    const formInputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.01)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn-submit, .auth-tab, .social-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.className = 'ripple';
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .btn-submit, .auth-tab, .social-btn {
            position: relative;
            overflow: hidden;
        }
    `;
    document.head.appendChild(style);
});
