// Mock Data (Fallback)
const LANGUAGES = [
    { name: "French", native: "Français", sample: "Excusez-moi, où est la bibliothèque?" },
    { name: "Spanish", native: "Español", sample: "Hola, ¿cómo estás hoy?" },
    { name: "Japanese", native: "日本語", sample: "すみません、駅はどこですか？" },
    { name: "German", native: "Deutsch", sample: "Entschuldigung, können Sie mir helfen?" },
    { name: "Italian", native: "Italiano", sample: "Vorrei un caffè, per favor." },
    { name: "Mandarin", native: "中文", sample: "你好，很高兴见到你。" },
    { name: "Portuguese", native: "Português", sample: "Onde fica a praia mais próxima?" }
];

// State
let isListening = false;
let history = [];
let mediaRecorder;
let audioChunks = [];

// DOM Elements
const listenBtn = document.getElementById('listen-btn');
const statusText = document.querySelector('.status-text');
const rippleContainer = document.querySelector('.ripple-container');
const viewHome = document.getElementById('view-home');
const viewResult = document.getElementById('view-result');
const resetBtn = document.getElementById('reset-btn');
const historyBtn = document.getElementById('history-btn');
const historyView = document.getElementById('view-history');
const closeHistoryBtn = document.getElementById('close-history');
const historyList = document.getElementById('history-list');

// Elements to update in Result
const langNameEl = document.getElementById('language-name');
const langNativeEl = document.getElementById('language-native');
const sampleTextEl = document.getElementById('sample-text');
const confidenceEl = document.querySelector('.confidence-badge');

// Event Listeners
listenBtn.addEventListener('click', toggleListening);
resetBtn.addEventListener('click', resetApp);
historyBtn.addEventListener('click', openHistory);
closeHistoryBtn.addEventListener('click', closeHistory);

function toggleListening() {
    if (isListening) return;
    startListening();
}

async function startListening() {
    isListening = true;
    statusText.textContent = "Listening...";
    rippleContainer.classList.add('listening');
    audioChunks = [];

    try {
        // Try to get real microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = handleAudioStop;
        mediaRecorder.start();

        // Auto-stop after 4 seconds (simulating "Shazam" listening window)
        setTimeout(() => {
            if (mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
                stopListeningUI();
            }
        }, 4000);

    } catch (err) {
        console.error("Microphone Error:", err);
        alert("Microphone access denied: " + err.message);
        // Fallback to pure simulation
        setTimeout(() => {
            stopListeningUI();
            // showResult(null); // Disable mock fallback for debugging
        }, 4000);
    }
}

function stopListeningUI() {
    isListening = false;
    statusText.textContent = "Analyzing...";
    rippleContainer.classList.remove('listening');
}

async function handleAudioStop() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('audio', audioBlob);

    try {
        // In production/mobile, this should point to your deployed backend (e.g., Render URL)
        // For local testing on device, use your computer's IP (e.g., http://192.168.1.5:3000)
        const API_URL = window.location.hostname === 'localhost' || window.location.protocol === 'file:'
            ? 'https://lingo-app-37g4.onrender.com' // Deployed Backend
            : ''; // Relative path for web deployment

        const endpoint = API_URL ? `${API_URL}/api/identify` : '/api/identify';

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Server error');
        }

        const data = await response.json();
        showResult(data); // Show real result

    } catch (err) {
        console.error("Backend Error:", err);
        alert("Error connecting to server: " + err.message);
        // showResult(null); // Disable mock fallback for debugging
    }

    // Stop all tracks to release mic
    if (mediaRecorder && mediaRecorder.stream) {
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}

function showResult(realData) {
    let result;
    let confidence;

    if (realData && realData.language) {
        // Format real data
        result = {
            name: realData.language, // e.g. "French"
            native: realData.language_native, // e.g. "Français"
            sample: realData.text || "Audio processed successfully.",
            translation: realData.translation || "Translation unavailable."
        };
        confidence = 99; // Whisper is usually very high
    } else {
        // Use Mock Data
        const mock = LANGUAGES[Math.floor(Math.random() * LANGUAGES.length)];
        result = {
            ...mock,
            translation: "This is a simulated translation."
        };
        confidence = 85 + Math.floor(Math.random() * 14);
    }

    // Update UI
    langNameEl.textContent = result.name;
    langNativeEl.textContent = result.native;
    sampleTextEl.textContent = `"${result.sample}"`;

    const translationEl = document.getElementById('translation-text');
    if (translationEl) {
        translationEl.textContent = `"${result.translation}"`;
    }

    confidenceEl.textContent = `${confidence}% Confidence`;

    // Switch Views
    viewHome.classList.remove('active');
    setTimeout(() => {
        viewResult.classList.add('active');
    }, 100);

    addToHistory(result);
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function resetApp() {
    viewResult.classList.remove('active');
    setTimeout(() => {
        viewHome.classList.add('active');
        statusText.textContent = "Tap to Listen";
    }, 100);
}

function addToHistory(lang) {
    const now = new Date();
    const timeString = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const item = {
        lang: lang.name,
        time: timeString
    };

    history.unshift(item);
    renderHistory();
}

function renderHistory() {
    historyList.innerHTML = '';
    history.forEach(item => {
        const li = document.createElement('li');
        li.className = 'history-item';
        li.innerHTML = `
            <span class="history-lang">${item.lang}</span>
            <span class="history-time">${item.time}</span>
        `;
        historyList.appendChild(li);
    });
}

function openHistory() {
    historyView.classList.add('open');
}

function closeHistory() {
    historyView.classList.remove('open');
}
