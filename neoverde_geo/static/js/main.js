// main.js - JavaScript principal para o site NeoVerde Geografia Interativa

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa os componentes da página
    initProjects();
    initGallery();
    initQuiz();
    initWeatherSearch();
});

// ===== GALERIA =====
function initGallery() {
    // Carrega as imagens da galeria
    fetchMedia('gallery');
}

// ===== PROJETOS =====
function initProjects() {
    // Carrega os projetos da API
    fetchMedia('projects');
    
    // Configura os filtros
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove a classe ativa de todos os botões
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Adiciona a classe ativa ao botão clicado
            this.classList.add('active');
            
            // Filtra os projetos
            const filter = this.getAttribute('data-filter');
            filterProjects(filter);
        });
    });
}

function fetchMedia(type) {
    // Define o container baseado no tipo
    const container = type === 'projects' ? '#projects-container' : '#gallery-container';
    
    // Mostra o spinner de carregamento
    document.querySelector(container).innerHTML = '<div class="loading-spinner"></div>';
    
    // Faz a requisição para a API
    fetch('/api/media')
        .then(response => response.json())
        .then(data => {
            // Renderiza os projetos ou a galeria baseado no tipo
            if (type === 'projects') {
                renderProjects(data);
            } else if (type === 'gallery') {
                renderGallery(data);
            }
        })
        .catch(error => {
            console.error(`Erro ao carregar ${type}:`, error);
            document.querySelector(container).innerHTML = `<p class="error-message">Erro ao carregar ${type}. Por favor, tente novamente.</p>`;
        });
}

function renderProjects(mediaItems) {
    const projectsContainer = document.querySelector('#projects-container');
    
    // Limpa o container
    projectsContainer.innerHTML = '';
    
    if (mediaItems.length === 0) {
        projectsContainer.innerHTML = '<p class="empty-message">Nenhum projeto encontrado.</p>';
        return;
    }
    
    // Filtra apenas os itens de mídia que são imagens
    const projects = mediaItems.filter(item => item.filetype.startsWith('image/'));
    
    // Renderiza cada projeto
    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        projectCard.setAttribute('data-category', project.category);
        
        projectCard.innerHTML = `
            <div class="project-image">
                <img src="${project.url}" alt="${project.description || 'Imagem do projeto'}">
            </div>
            <div class="project-content">
                <span class="project-category">${project.category}</span>
                <h3 class="project-title">${project.filename}</h3>
                <p class="project-description">${project.description || 'Sem descrição disponível'}</p>
            </div>
        `;
        
        projectsContainer.appendChild(projectCard);
    });
}

function filterProjects(filter) {
    const projects = document.querySelectorAll('.project-card');
    
    projects.forEach(project => {
        if (filter === 'all' || project.getAttribute('data-category') === filter) {
            project.style.display = 'block';
        } else {
            project.style.display = 'none';
        }
    });
}

// ===== GALERIA =====
function renderGallery(mediaItems) {
    const galleryContainer = document.querySelector('#gallery-container');
    
    // Limpa o container
    galleryContainer.innerHTML = '';
    
    if (mediaItems.length === 0) {
        galleryContainer.innerHTML = '<p class="empty-message">Nenhuma mídia encontrada.</p>';
        return;
    }
    
    // Renderiza cada item da galeria
    mediaItems.forEach(item => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        
        // Verifica se é uma imagem ou vídeo
        if (item.filetype.startsWith('image/')) {
            galleryItem.innerHTML = `
                <img src="${item.url}" alt="${item.description || 'Imagem da galeria'}">
                <div class="gallery-overlay">
                    <h3 class="gallery-title">${item.filename}</h3>
                    <span class="gallery-category">${item.category}</span>
                </div>
            `;
        } else if (item.filetype.startsWith('video/')) {
            galleryItem.innerHTML = `
                <video src="${item.url}" poster="/static/images/video-poster.jpg" controls></video>
                <div class="gallery-overlay">
                    <h3 class="gallery-title">${item.filename}</h3>
                    <span class="gallery-category">${item.category}</span>
                </div>
            `;
        }
        
        galleryContainer.appendChild(galleryItem);
        
        // Adiciona evento de clique para abrir o modal
        galleryItem.addEventListener('click', function() {
            openGalleryModal(item);
        });
    });
}

function openGalleryModal(item) {
    // Implementação futura para o modal da galeria
    console.log('Abrir modal para:', item);
}

// ===== QUIZ =====
function initQuiz() {
    // Dados do quiz
    const quizData = [
        {
            question: "Qual é o maior país do mundo em área territorial?",
            options: ["Rússia", "China", "Estados Unidos", "Brasil"],
            answer: 0,
            explanation: "A Rússia é o maior país do mundo com uma área de aproximadamente 17 milhões de km²."
        },
        {
            question: "Qual é o rio mais longo do mundo?",
            options: ["Nilo", "Amazonas", "Yangtzé", "Mississippi"],
            answer: 1,
            explanation: "O rio Amazonas é considerado o mais longo do mundo com aproximadamente 6.992 km de extensão."
        },
        {
            question: "Qual é o ponto mais alto da Terra?",
            options: ["Monte Kilimanjaro", "Monte Everest", "Monte Aconcágua", "K2"],
            answer: 1,
            explanation: "O Monte Everest é o ponto mais alto da Terra, com 8.848 metros acima do nível do mar."
        },
        {
            question: "Qual é o maior oceano do mundo?",
            options: ["Atlântico", "Índico", "Pacífico", "Ártico"],
            answer: 2,
            explanation: "O Oceano Pacífico é o maior oceano do mundo, cobrindo mais de 30% da superfície terrestre."
        },
        {
            question: "Qual é o país com a maior população do mundo?",
            options: ["Índia", "China", "Estados Unidos", "Indonésia"],
            answer: 1,
            explanation: "A China é o país mais populoso do mundo, com mais de 1,4 bilhão de habitantes."
        }
    ];
    
    let currentQuestion = 0;
    let score = 0;
    let quizStarted = false;
    
    // Elementos do DOM
    const startButton = document.getElementById('start-quiz');
    const quizQuestions = document.querySelector('.quiz-questions');
    const quizResults = document.querySelector('.quiz-results');
    const questionText = document.getElementById('question-text');
    const optionButtons = document.querySelectorAll('.option-btn');
    const feedbackText = document.getElementById('feedback-text');
    const feedbackDiv = document.querySelector('.quiz-feedback');
    const nextButton = document.getElementById('next-question');
    const currentQuestionSpan = document.getElementById('current-question');
    const totalQuestionsSpan = document.getElementById('total-questions');
    const totalQuestionsResultSpan = document.getElementById('total-questions-result');
    const correctAnswersSpan = document.getElementById('correct-answers');
    const restartButton = document.getElementById('restart-quiz');
    
    // Inicializa o quiz
    function initializeQuiz() {
        // Define o número total de perguntas
        totalQuestionsSpan.textContent = quizData.length;
        totalQuestionsResultSpan.textContent = quizData.length;
        
        // Configura o botão de início
        startButton.addEventListener('click', startQuiz);
        
        // Configura o botão de próxima pergunta
        nextButton.addEventListener('click', nextQuestion);
        
        // Configura o botão de reiniciar
        restartButton.addEventListener('click', restartQuiz);
        
        // Configura os botões de opção
        optionButtons.forEach(button => {
            button.addEventListener('click', checkAnswer);
        });
    }
    
    // Inicia o quiz
    function startQuiz() {
        quizStarted = true;
        currentQuestion = 0;
        score = 0;
        
        document.querySelector('.quiz-start').style.display = 'none';
        quizQuestions.style.display = 'block';
        quizResults.style.display = 'none';
        
        loadQuestion();
    }
    
    // Carrega a pergunta atual
    function loadQuestion() {
        const question = quizData[currentQuestion];
        
        questionText.textContent = question.question;
        currentQuestionSpan.textContent = currentQuestion + 1;
        
        optionButtons.forEach((button, index) => {
            button.textContent = question.options[index];
            button.classList.remove('correct', 'incorrect');
            button.disabled = false;
        });
        
        feedbackDiv.style.display = 'none';
    }
    
    // Verifica a resposta selecionada
    function checkAnswer() {
        if (!quizStarted) return;
        
        const selectedOption = parseInt(this.getAttribute('data-index'));
        const question = quizData[currentQuestion];
        
        // Desabilita todos os botões
        optionButtons.forEach(button => {
            button.disabled = true;
        });
        
        // Verifica se a resposta está correta
        if (selectedOption === question.answer) {
            this.classList.add('correct');
            feedbackText.textContent = `Correto! ${question.explanation}`;
            score++;
        } else {
            this.classList.add('incorrect');
            optionButtons[question.answer].classList.add('correct');
            feedbackText.textContent = `Incorreto. ${question.explanation}`;
        }
        
        feedbackDiv.style.display = 'block';
    }
    
    // Avança para a próxima pergunta
    function nextQuestion() {
        currentQuestion++;
        
        if (currentQuestion < quizData.length) {
            loadQuestion();
        } else {
            showResults();
        }
    }
    
    // Mostra os resultados do quiz
    function showResults() {
        quizQuestions.style.display = 'none';
        quizResults.style.display = 'block';
        
        correctAnswersSpan.textContent = score;
    }
    
    // Reinicia o quiz
    function restartQuiz() {
        startQuiz();
    }
    
    // Inicializa o quiz
    initializeQuiz();
}

// ===== CLIMA =====
function initWeatherSearch() {
    const searchButton = document.getElementById('search-weather');
    const cityInput = document.getElementById('city-search');
    const weatherResults = document.getElementById('weather-results');
    const weatherError = document.getElementById('weather-error');
    
    // Configura o botão de busca
    searchButton.addEventListener('click', function() {
        const city = cityInput.value.trim();
        
        if (city) {
            searchWeather(city);
        }
    });
    
    // Configura o evento de tecla Enter
    cityInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const city = cityInput.value.trim();
            
            if (city) {
                searchWeather(city);
            }
        }
    });
    
    // Função para buscar dados climáticos
    function searchWeather(city) {
        // Simulação de dados climáticos (em um projeto real, seria uma chamada de API)
        simulateWeatherData(city);
    }
    
    // Simulação de dados climáticos
    function simulateWeatherData(city) {
        // Mostra o spinner de carregamento
        weatherResults.innerHTML = '<div class="loading-spinner"></div>';
        weatherResults.style.display = 'block';
        weatherError.style.display = 'none';
        
        // Simula uma chamada de API com timeout
        setTimeout(() => {
            // Gera dados aleatórios para simulação
            const temperature = Math.floor(Math.random() * 35) + 5; // 5 a 40°C
            const humidity = Math.floor(Math.random() * 60) + 30; // 30% a 90%
            const wind = Math.floor(Math.random() * 30) + 5; // 5 a 35 km/h
            const pressure = Math.floor(Math.random() * 50) + 980; // 980 a 1030 hPa
            
            // Possíveis descrições do clima
            const descriptions = ['Céu limpo', 'Parcialmente nublado', 'Nublado', 'Chuva leve', 'Chuva forte', 'Tempestade', 'Neve'];
            const description = descriptions[Math.floor(Math.random() * descriptions.length)];
            
            // Atualiza os elementos do DOM
            document.getElementById('weather-city').textContent = city;
            document.getElementById('weather-date').textContent = new Date().toLocaleDateString('pt-BR');
            document.getElementById('weather-temp-value').textContent = temperature;
            document.getElementById('weather-description').textContent = description;
            document.getElementById('weather-humidity').textContent = `${humidity}%`;
            document.getElementById('weather-wind').textContent = `${wind} km/h`;
            document.getElementById('weather-pressure').textContent = `${pressure} hPa`;
            
            // Define o ícone do clima
            let iconUrl = '';
            if (description.includes('limpo')) {
                iconUrl = 'https://openweathermap.org/img/wn/01d@2x.png';
            } else if (description.includes('Parcialmente')) {
                iconUrl = 'https://openweathermap.org/img/wn/02d@2x.png';
            } else if (description.includes('nublado')) {
                iconUrl = 'https://openweathermap.org/img/wn/03d@2x.png';
            } else if (description.includes('Chuva leve')) {
                iconUrl = 'https://openweathermap.org/img/wn/10d@2x.png';
            } else if (description.includes('Chuva forte')) {
                iconUrl = 'https://openweathermap.org/img/wn/09d@2x.png';
            } else if (description.includes('Tempestade')) {
                iconUrl = 'https://openweathermap.org/img/wn/11d@2x.png';
            } else if (description.includes('Neve')) {
                iconUrl = 'https://openweathermap.org/img/wn/13d@2x.png';
            }
            
            document.getElementById('weather-icon-img').src = iconUrl;
            
            // Mostra os resultados
            weatherResults.style.display = 'block';
        }, 1000);
    }
}