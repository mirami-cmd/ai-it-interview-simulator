// app.js – client logic for AI IT Interview Simulator
const BACKEND_URL = "https://discozet.pythonanywhere.com"; // placeholder – will be replaced after deploy

let currentQuestion = 0;
let questions = [];

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function startInterview() {
    // Example payload – replace with actual user input later
    fetch(`${BACKEND_URL}/api/interview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ direction: 'backend', grade: 'middle', email: 'test@example.com' })
    })
    .then(r => r.json())
    .then(data => {
        questions = data.questions || [];
        currentQuestion = 0;
        if (questions.length) displayQuestion();
        else finish();
    })
    .catch(err => {
        console.error('Error', err);
        document.getElementById('result-text').textContent = 'Ошибка сервера';
        showScreen('screen-result');
    });
}

function displayQuestion() {
    // 30% chance to suggest premium after showing a question
    if (Math.random() < 0.3) {
        // Slight delay to let user see the question first
        setTimeout(openPremium, 500);
    }
    document.getElementById('question-title').textContent = questions[currentQuestion];
    document.getElementById('answer').value = '';
    showScreen('screen-interview');
}

function nextQuestion() {
    currentQuestion++;
    // After 30% of the interview questions, block further progress and prompt premium purchase
    if (currentQuestion >= Math.ceil(questions.length * 0.3)) {
        // Show premium modal and stop the interview
        openPremium();
        // Optionally, clear remaining questions to prevent further navigation
        return;
    }
    if (currentQuestion < questions.length) {
        displayQuestion();
    } else {
        finish();
    }
}

function finish() {
    document.getElementById('result-text').textContent = "Интервью завершено. Спасибо за участие!";
    document.getElementById('result-text').textContent = "Интервью завершено. Оцените себя и подумайте о премиуме!";
    showScreen('screen-result');
}

function openPremium() {
    document.getElementById('premium-modal').classList.remove('hidden');
}
function closePremium() {
    document.getElementById('premium-modal').classList.add('hidden');
}

// Event listeners
document.getElementById('start-btn')?.addEventListener('click', startInterview);
document.getElementById('next-btn')?.addEventListener('click', nextQuestion);
document.getElementById('premium-btn')?.addEventListener('click', openPremium);
document.getElementById('close-modal')?.addEventListener('click', closePremium);
