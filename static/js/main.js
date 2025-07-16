// Stan aplikacji
let chatHistory = [
    {
        role: "system",
        content: "Jesteś profesjonalnym terapeutą CBT (Cognitive Behavioral Therapy). Twoim zadaniem jest prowadzenie sesji terapeutycznej, pomaganie w identyfikacji myśli automatycznych, emocji, zachowań i zniekształceń poznawczych. Zadawaj pytania, które pomogą pacjentowi zrozumieć swoje wzorce myślowe i wypracować zdrowsze sposoby radzenia sobie z problemami. Bądź empatyczny, profesjonalny i wspierający."
    }
];

let currentToken = null;

// Inicjalizacja aplikacji
document.addEventListener('DOMContentLoaded', function() {
    // Sprawdź czy użytkownik jest już zalogowany
    currentToken = localStorage.getItem('authToken');
    if (currentToken) {
        showAppInterface();
    } else {
        showAuthInterface();
    }

    // Event listenery dla formularzy uwierzytelniania
    setupAuthForms();

    // Event listenery dla interfejsu aplikacji
    setupAppInterface();
});

function setupAuthForms() {
    // Przełączanie między formularzami
    document.getElementById('show-register').addEventListener('click', function(e) {
        e.preventDefault();
        showRegister();
    });

    document.getElementById('show-login').addEventListener('click', function(e) {
        e.preventDefault();
        showLogin();
    });

    // Obsługa rejestracji
    document.getElementById('register-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await handleRegister(e);
    });

    // Obsługa logowania
    document.getElementById('login-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        await handleLogin(e);
    });
}

function setupAppInterface() {
    // Menu hamburgerowe
    document.getElementById('menu-toggle').addEventListener('click', function() {
        toggleMenu();
    });

    // Zamknij menu po kliknięciu poza nim
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.nav-menu')) {
            document.getElementById('nav-dropdown').classList.remove('show');
        }
    });

    // Nowa rozmowa
    document.getElementById('new-chat').addEventListener('click', function() {
        startNewChat();
    });

    // Wylogowanie
    document.getElementById('logout').addEventListener('click', function() {
        logout();
    });
}

function showRegister() {
    document.getElementById('login-section').classList.remove('active');
    document.getElementById('register-section').classList.add('active');
}

function showLogin() {
    document.getElementById('register-section').classList.remove('active');
    document.getElementById('login-section').classList.add('active');
}

async function handleRegister(e) {
    const formData = new FormData(e.target);
    const userData = {
        email: formData.get('email'),
        password: formData.get('password'),
        username: formData.get('username') || null
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            showNotification('Rejestracja udana! Możesz się teraz zalogować.', 'success');
            showLogin();
            document.getElementById('register-form').reset();
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Błąd podczas rejestracji', 'error');
        }
    } catch (error) {
        showNotification('Błąd połączenia z serwerem', 'error');
    }
}

async function handleLogin(e) {
    const formData = new FormData(e.target);
    const loginData = new FormData();
    loginData.append('username', formData.get('email')); // FastAPI OAuth2 oczekuje 'username'
    loginData.append('password', formData.get('password'));

    try {
        const response = await fetch('/token', {
            method: 'POST',
            body: loginData
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            localStorage.setItem('authToken', currentToken);
            showAppInterface();
            showNotification('Zalogowano pomyślnie!', 'success');
        } else {
            const error = await response.json();
            showNotification(error.detail || 'Błąd podczas logowania', 'error');
        }
    } catch (error) {
        showNotification('Błąd połączenia z serwerem', 'error');
    }
}

function showAuthInterface() {
    document.getElementById('auth-container').classList.remove('hidden');
    document.getElementById('app-container').classList.add('hidden');
}

function showAppInterface() {
    document.getElementById('auth-container').classList.add('hidden');
    document.getElementById('app-container').classList.remove('hidden');
    showChatView();
}

function showChatView() {
    document.getElementById('main-content-area').innerHTML = `
        <div id="chat-view" class="chat-view">
            <div id="chat-container" class="chat-container">
                <!-- Wiadomości będą dodawane tutaj dynamicznie -->
            </div>

            <div class="chat-input-area">
                <form id="chat-form" class="chat-form">
                    <input type="text" id="chat-input" placeholder="Napisz swoją wiadomość..." required>
                    <button type="submit" class="btn-send">Wyślij</button>
                </form>
                <button id="end-session" class="btn-secondary">Zakończ i Zapisz Refleksję</button>
            </div>
        </div>
    `;

    // Ponownie dodaj event listenery
    setupChatEventListeners();
}

function setupChatEventListeners() {
    const chatForm = document.getElementById('chat-form');
    const endSessionBtn = document.getElementById('end-session');

    if (chatForm) {
        chatForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            await sendMessage();
        });
    }
    if (endSessionBtn) {
        endSessionBtn.addEventListener('click', async function() {
            await endChatSession();
        });
    }
}

function resetChat() {
    chatHistory = [
        {
            role: "system",
            content: "Jesteś profesjonalnym terapeutą CBT (Cognitive Behavioral Therapy). Twoim zadaniem jest prowadzenie sesji terapeutycznej, pomaganie w identyfikacji myśli automatycznych, emocji, zachowań i zniekształceń poznawczych. Zadawaj pytania, które pomogą pacjentowi zrozumieć swoje wzorce myślowe i wypracować zdrowsze sposoby radzenia sobie z problemami. Bądź empatyczny, profesjonalny i wspierający."
        }
    ];

    const chatContainer = document.getElementById('chat-container');
    if (chatContainer) {
        chatContainer.innerHTML = '';
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();

    if (!message) return;

    // Dodaj wiadomość użytkownika do historii i wyświetl
    const userMessage = { role: "user", content: message };
    chatHistory.push(userMessage);
    displayMessage(userMessage);

    // Wyczyść input
    input.value = '';

    try {
        // Wyślij do API
        const response = await fetch('/chat/conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ history: chatHistory })
        });

        if (response.ok) {
            const data = await response.json();
            const assistantMessage = data.message;

            // Dodaj odpowiedź asystenta do historii i wyświetl
            chatHistory.push(assistantMessage);
            displayMessage(assistantMessage);
        } else if (response.status === 401) {
            showNotification('Sesja wygasła. Zaloguj się ponownie.', 'error');
            logout();
        } else {
            showNotification('Błąd podczas komunikacji z AI', 'error');
        }
    } catch (error) {
        showNotification('Błąd połączenia z serwerem', 'error');
    }
}

function displayMessage(message) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${message.role}`;

    if (message.role !== 'system') {
        messageDiv.innerHTML = `
            <div class="message-content">
                <span class="message-text">${message.content}</span>
                <span class="message-role">${message.role === 'user' ? 'Ty' : 'Terapeuta'}</span>
            </div>
        `;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

async function endChatSession() {
    if (chatHistory.length <= 1) {
        showNotification('Brak rozmowy do zapisania', 'warning');
        return;
    }

    try {
        const response = await fetch('/chat/end_session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ history: chatHistory })
        });

        if (response.ok) {
            showNotification('Sesja została zapisana w dzienniku!', 'success');
            resetChat();
        } else if (response.status === 401) {
            showNotification('Sesja wygasła. Zaloguj się ponownie.', 'error');
            logout();
        } else {
            showNotification('Błąd podczas zapisywania sesji', 'error');
        }
    } catch (error) {
        showNotification('Błąd połączenia z serwerem', 'error');
    }
}

function startNewChat() {
    showChatView();
    resetChat();
    toggleMenu();
    showNotification('Rozpoczęto nową rozmowę', 'success');
}

function toggleMenu() {
    const dropdown = document.getElementById('nav-dropdown');
    dropdown.classList.toggle('show');
}

function logout() {
    localStorage.removeItem('authToken');
    currentToken = null;
    showAuthInterface();
    resetChat();
    showNotification('Zostałeś wylogowany', 'success');
}

function showNotification(message, type = 'info') {
    const notificationArea = document.getElementById('notification-area');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    notificationArea.appendChild(notification);

    // Usuń po 5 sekundach
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Konfiguracja HTMX - dodaj token do wszystkich requestów
document.body.addEventListener('htmx:configRequest', function(evt) {
    const token = localStorage.getItem('authToken');
    if (token) {
        evt.detail.headers['Authorization'] = `Bearer ${token}`;
    }
});

// Obsługa błędów 401 - przekieruj do logowania
document.body.addEventListener('htmx:responseError', function(evt) {
    if (evt.detail.xhr.status === 401) {
        console.log('Unauthorized access - redirecting to login');
        logout();
    }
});

// Obsługa usuwania wpisu z dziennika - odśwież listę po usunięciu
document.body.addEventListener('htmx:afterRequest', function(evt) {
    // Sprawdź czy to było żądanie DELETE do /diaries/
    if (evt.detail.requestConfig.verb === 'delete' && 
        evt.detail.requestConfig.path.startsWith('/diaries/') &&
        evt.detail.xhr.status === 204) {
        
        // Odśwież listę dziennika jeśli jest widoczna
        const mainContent = document.getElementById('main-content-area');
        if (mainContent && mainContent.innerHTML.includes('diary-list')) {
            // Wykonaj żądanie odświeżenia listy dziennika
            fetch('/ui/diaries', {
                headers: {
                    'Authorization': `Bearer ${currentToken}`
                }
            })
            .then(response => response.text())
            .then(html => {
                mainContent.innerHTML = html;
                showNotification('Wpis został usunięty', 'success');
            })
            .catch(error => {
                console.error('Błąd podczas odświeżania listy:', error);
                showNotification('Wpis został usunięty, ale lista może wymagać odświeżenia', 'warning');
            });
        }
    }
});