// Sign Language Conversion Functions

// Main Sign Language Conversion Function
async function convertToSignLanguage() {
    const text = document.getElementById('signInputText').value.trim();
    
    if (!text) {
        showError('Vui lòng nhập văn bản cần chuyển đổi!');
        return;
    }
    
    showSignLoading(true);
    hideError();
    hideSignResults();
    
    try {
        const response = await fetch(`${API_BASE_URL}/convert-sign-language`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        showSignLoading(false);
        
        if (response.ok && data.success) {
            displaySignResults(data);
        } else {
            showError(data.error || 'Có lỗi xảy ra khi chuyển đổi!');
        }
    } catch (error) {
        showSignLoading(false);
        showError('Lỗi kết nối API: ' + error.message);
        checkAPIHealth();
    }
}

// Loading Functions for Sign Language
function showSignLoading(show) {
    const loading = document.getElementById('signLoading');
    const btn = document.getElementById('convertSignBtn');
    
    if (show) {
        loading.style.display = 'block';
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang chuyển đổi...';
    } else {
        loading.style.display = 'none';
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-hands"></i> Chuyển đổi sang Ký hiệu';
    }
}

// Sign Language Results Display
function hideSignResults() {
    document.getElementById('signResultsSection').style.display = 'none';
}

function displaySignResults(data) {
    // Hiển thị câu gốc
    document.getElementById('originalSentence').textContent = data.original_sentence;
    
    // Hiển thị chuỗi ký hiệu
    const signSequenceDiv = document.getElementById('signSequence');
    signSequenceDiv.innerHTML = '<strong>' + data.sign_language_sequence.join(' → ') + '</strong>';
    
    // Hiển thị bảng phân tích từ chi tiết với thông tin từ điển
    const wordDetailsBody = document.getElementById('wordDetailsBody');
    wordDetailsBody.innerHTML = '';
    
    if (data.word_details && data.word_details.length > 0) {
        data.word_details.forEach(word_detail => {
            const row = document.createElement('tr');
            
            // Tạo class cho hành động dựa trên việc có trong từ điển hay không
            const actionClass = word_detail.in_dictionary ? 'text-success fw-bold' : 'text-muted';
            const actionIcon = word_detail.in_dictionary ? '<i class="fas fa-book me-1"></i>' : '<i class="fas fa-tag me-1"></i>';
            
            row.innerHTML = `
                <td>${word_detail.index}</td>
                <td><strong>${word_detail.original_word}</strong></td>
                <td><span class="word-tag tag-${word_detail.pos_tag}">${word_detail.pos_tag}</span></td>
                <td class="${actionClass}">
                    ${actionIcon}${word_detail.dictionary_action}
                    ${word_detail.in_dictionary ? '<small class="text-success ms-2">(có trong từ điển)</small>' : '<small class="text-muted ms-2">(tạo từ POS tag)</small>'}
                </td>
            `;
            wordDetailsBody.appendChild(row);
        });
    } else {
        // Fallback to old method if word_details is not available
        data.pos_analysis.forEach(([word, tag], index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td><strong>${word}</strong></td>
                <td><span class="word-tag tag-${tag}">${tag}</span></td>
                <td class="text-muted"><i class="fas fa-tag me-1"></i>${word.toUpperCase()}[${tag}] <small class="text-muted ms-2">(tạo từ POS tag)</small></td>
            `;
            wordDetailsBody.appendChild(row);
        });
    }
    
    // Hiển thị cấu trúc phân tích
    const structureDiv = document.getElementById('structureAnalysis');
    const structure = data.structure_analysis.structure_changes;
    
    structureDiv.innerHTML = `
        <div class="col-md-3">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <h5>${structure.subjects}</h5>
                    <small>Chủ ngữ</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <h5>${structure.verbs}</h5>
                    <small>Động từ</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <h5>${structure.objects}</h5>
                    <small>Tân ngữ</small>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card bg-warning text-white">
                <div class="card-body text-center">
                    <h5>${structure.adjectives}</h5>
                    <small>Tính từ</small>
                </div>
            </div>
        </div>
    `;
    
    // Hiển thị section kết quả
    document.getElementById('signResultsSection').style.display = 'block';
    
    // Scroll to results
    document.getElementById('signResultsSection').scrollIntoView({ 
        behavior: 'smooth' 
    });
}
function displayGrammarAnalysis(grammarAnalysis) {
    // Tạo section mới cho grammar analysis nếu chưa có
    let grammarSection = document.getElementById('grammarAnalysisSection');
    if (!grammarSection) {
        grammarSection = document.createElement('div');
        grammarSection.id = 'grammarAnalysisSection';
        grammarSection.className = 'mt-4';
        grammarSection.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h6><i class="fas fa-microscope"></i> Phân tích ngữ pháp chi tiết</h6>
                </div>
                <div class="card-body" id="grammarAnalysisContent">
                </div>
            </div>
        `;
        
        // Thêm vào sau phần cấu trúc phân tích
        const structureSection = document.getElementById('structureAnalysis');
        structureSection.parentNode.insertBefore(grammarSection, structureSection.nextSibling);
    }
    
    const contentDiv = document.getElementById('grammarAnalysisContent');
    const analysis = grammarAnalysis.grammar_analysis;
    
    contentDiv.innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <h6><i class="fas fa-language"></i> Cấu trúc Tiếng Việt:</h6>
                <div class="alert alert-info">
                    <strong>Thứ tự từ:</strong> ${analysis.differences.word_order_change.vietnamese}<br>
                    <strong>Ví dụ:</strong> "Tôi ăn cơm"
                </div>
            </div>
            <div class="col-md-6">
                <h6><i class="fas fa-hands"></i> Cấu trúc Ngôn ngữ Ký hiệu:</h6>
                <div class="alert alert-success">
                    <strong>Thứ tự từ:</strong> ${analysis.differences.word_order_change.sign_language}<br>
                    <strong>Ví dụ:</strong> "TÔI CƠM ĂN"
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-12">
                <h6><i class="fas fa-exchange-alt"></i> Quy tắc chuyển đổi đã áp dụng:</h6>
                <div class="list-group">
                    ${analysis.conversion_applied.map(rule => `
                        <div class="list-group-item">
                            <strong>${rule.rule}:</strong> ${rule.description}
                            <br><small class="text-muted">Ví dụ: ${rule.example}</small>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-12">
                <h6><i class="fas fa-lightbulb"></i> Thông tin giáo dục:</h6>
                <div class="alert alert-warning">
                    ${grammarAnalysis.educational_insights.map(insight => `
                        <div>${insight}</div>
                    `).join('')}
                </div>
            </div>
        </div>
        
        <div class="row mt-3">
            <div class="col-md-6">
                <div class="card bg-light">
                    <div class="card-body text-center">
                        <h5>${grammarAnalysis.conversion_summary.complexity_score}</h5>
                        <small>Điểm phức tạp câu</small>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card bg-light">
                    <div class="card-body text-center">
                        <h5>${grammarAnalysis.conversion_summary.structural_changes}</h5>
                        <small>Số thay đổi cấu trúc</small>
                    </div>
                </div>
            </div>
        </div>
    `;
}
