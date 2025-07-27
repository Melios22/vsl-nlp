// POS Tagging Functions

// Main POS Analysis Function
async function analyzeText() {
    const text = document.getElementById('inputText').value.trim();
    
    if (!text) {
        showError('Vui lòng nhập văn bản cần phân tích!');
        return;
    }
    
    showPosLoading(true);
    hideError();
    hidePosResults();
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        showPosLoading(false);
        
        if (response.ok && data.success) {
            displayPosResults(data.results, data.statistics);
        } else {
            showError(data.error || 'Có lỗi xảy ra khi phân tích!');
        }
    } catch (error) {
        showPosLoading(false);
        showError('Lỗi kết nối API: ' + error.message);
        checkAPIHealth();
    }
}

// Loading Functions for POS
function showPosLoading(show) {
    const loading = document.getElementById('posLoading');
    const btn = document.getElementById('analyzeBtn');
    
    if (show) {
        loading.style.display = 'block';
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang phân tích...';
    } else {
        loading.style.display = 'none';
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-search"></i> Phân tích POS';
    }
}

// POS Results Display
function hidePosResults() {
    document.getElementById('posResultsSection').style.display = 'none';
}

function displayPosResults(results, stats) {
    // Hiển thị thống kê
    document.getElementById('totalWords').textContent = stats.total_words;
    document.getElementById('uniqueTags').textContent = stats.unique_tags;
    document.getElementById('processingTime').textContent = stats.processing_time + 's';
    document.getElementById('wordsPerSecond').textContent = stats.words_per_second;
    
    // Hiển thị văn bản được gán nhãn
    const taggedTextDiv = document.getElementById('taggedText');
    taggedTextDiv.innerHTML = '';
    
    results.forEach(([word, tag]) => {
        const span = document.createElement('span');
        span.className = `word-tag tag-${tag}`;
        span.innerHTML = `${word} <span class="tag-label">${tag}</span>`;
        taggedTextDiv.appendChild(span);
        taggedTextDiv.appendChild(document.createTextNode(' '));
    });
    
    // Hiển thị bảng
    const tableBody = document.getElementById('resultsTable');
    tableBody.innerHTML = '';
    
    results.forEach(([word, tag], index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><strong>${word}</strong></td>
            <td><span class="word-tag tag-${tag}">${tag}</span></td>
        `;
        tableBody.appendChild(row);
    });
    
    // Hiển thị section kết quả
    document.getElementById('posResultsSection').style.display = 'block';
    
    // Scroll to results
    document.getElementById('posResultsSection').scrollIntoView({ 
        behavior: 'smooth' 
    });
}
