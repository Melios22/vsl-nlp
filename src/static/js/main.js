// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    checkAPIHealth();
    loadExamples();
    loadSignDictionaryInfo();
    initializeEventListeners();
});

// API Health Check
async function checkAPIHealth() {
    const statusBadge = document.getElementById('apiStatus');
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusBadge.className = 'badge bg-success';
            let statusText = '<i class="fas fa-check-circle"></i> API Ready';
            if (data.pos_tagger_loaded && data.sign_converter_loaded) {
                statusText = '<i class="fas fa-check-circle"></i> All Models Ready';
            }
            statusBadge.innerHTML = statusText;
        } else {
            statusBadge.className = 'badge bg-warning';
            statusBadge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> API Warning';
        }
    } catch (error) {
        statusBadge.className = 'badge bg-danger';
        statusBadge.innerHTML = '<i class="fas fa-times-circle"></i> API Offline';
    }
}

// Load Examples
async function loadExamples() {
    try {
        const response = await fetch(`${API_BASE_URL}/examples`);
        const data = await response.json();
        
        // Load examples for both tabs
        const posSelect = document.getElementById('exampleSelect');
        const signSelect = document.getElementById('signExampleSelect');
        
        data.examples.forEach(example => {
            // POS tab
            const posOption = document.createElement('option');
            posOption.value = example;
            posOption.textContent = example;
            posSelect.appendChild(posOption);
            
            // Sign tab
            const signOption = document.createElement('option');
            signOption.value = example;
            signOption.textContent = example;
            signSelect.appendChild(signOption);
        });
    } catch (error) {
        console.error('Error loading examples:', error);
    }
}

// Load Sign Dictionary Info
async function loadSignDictionaryInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/sign-dictionary-info`);
        const data = await response.json();
        
        const statsDiv = document.getElementById('dictionaryStats');
        statsDiv.innerHTML = `
            <div class="row text-center">
                <div class="col-6">
                    <strong>${data.total_entries}</strong><br>
                    <small>Tổng từ vựng</small>
                </div>
                <div class="col-6">
                    <strong>${data.categories.verbs}</strong><br>
                    <small>Động từ</small>
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading dictionary info:', error);
    }
}

// Initialize Event Listeners
function initializeEventListeners() {
    // POS Tagging Event Listeners
    document.getElementById('exampleSelect').addEventListener('change', function() {
        document.getElementById('inputText').value = this.value;
    });
    
    document.getElementById('analyzeBtn').addEventListener('click', analyzeText);
    
    document.getElementById('inputText').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            analyzeText();
        }
    });
    
    // Sign Language Conversion Event Listeners
    document.getElementById('signExampleSelect').addEventListener('change', function() {
        document.getElementById('signInputText').value = this.value;
    });
    
    document.getElementById('convertSignBtn').addEventListener('click', convertToSignLanguage);
    
    document.getElementById('signInputText').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            convertToSignLanguage();
        }
    });
}

// Error Handling
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Periodic API health check
setInterval(checkAPIHealth, 30000); // Check every 30 seconds
