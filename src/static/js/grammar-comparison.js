// Grammar Comparison functionality
class GrammarComparison {
    constructor() {
        this.init();
    }

    init() {
        // Load grammar comparison data when the tab is shown
        document.getElementById('grammar-tab').addEventListener('shown.bs.tab', () => {
            this.loadGrammarComparison();
        });
    }

    async loadGrammarComparison() {
        try {
            const response = await fetch('/api/grammar-comparison');
            const data = await response.json();
            
            if (response.ok) {
                this.displayGrammarComparison(data);
            } else {
                this.showError('Không thể tải thông tin so sánh ngữ pháp');
            }
        } catch (error) {
            console.error('Error loading grammar comparison:', error);
            this.showError('Lỗi kết nối khi tải thông tin so sánh ngữ pháp');
        }
    }

    displayGrammarComparison(data) {
        // Display Vietnamese grammar info
        this.displayVietnameseGrammar(data.vietnamese_structure);
        
        // Display Sign Language grammar info
        this.displaySignLanguageGrammar(data.sign_language_structure);
        
        // Display conversion rules
        this.displayConversionRules(data.conversion_rules);
        
        // Display key differences
        this.displayKeyDifferences(data.key_differences);
    }

    displayVietnameseGrammar(structure) {
        const container = document.getElementById('vietnameseGrammarInfo');
        
        const html = `
            <div class="mb-3">
                <h6 class="text-primary"><i class="fas fa-info-circle"></i> Cấu trúc cơ bản</h6>
                <div class="alert alert-primary">
                    <strong>Thứ tự từ:</strong> ${structure.word_order}
                </div>
            </div>
            
            <div class="mb-3">
                <h6 class="text-primary"><i class="fas fa-list"></i> Đặc điểm chính</h6>
                <ul class="list-group list-group-flush">
                    ${structure.characteristics.map(char => 
                        `<li class="list-group-item">${char}</li>`
                    ).join('')}
                </ul>
            </div>
            
            <div class="mb-3">
                <h6 class="text-primary"><i class="fas fa-code"></i> Ví dụ</h6>
                <div class="border rounded p-3 bg-light">
                    <strong>Câu:</strong> ${structure.example.sentence}<br>
                    <strong>Phân tích:</strong> ${structure.example.analysis}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displaySignLanguageGrammar(structure) {
        const container = document.getElementById('signLanguageGrammarInfo');
        
        const html = `
            <div class="mb-3">
                <h6 class="text-success"><i class="fas fa-info-circle"></i> Cấu trúc cơ bản</h6>
                <div class="alert alert-success">
                    <strong>Thứ tự từ:</strong> ${structure.word_order}
                </div>
            </div>
            
            <div class="mb-3">
                <h6 class="text-success"><i class="fas fa-list"></i> Đặc điểm chính</h6>
                <ul class="list-group list-group-flush">
                    ${structure.characteristics.map(char => 
                        `<li class="list-group-item">${char}</li>`
                    ).join('')}
                </ul>
            </div>
            
            <div class="mb-3">
                <h6 class="text-success"><i class="fas fa-code"></i> Ví dụ</h6>
                <div class="border rounded p-3 bg-light">
                    <strong>Câu:</strong> ${structure.example.sentence}<br>
                    <strong>Phân tích:</strong> ${structure.example.analysis}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayConversionRules(rules) {
        const container = document.getElementById('conversionRulesInfo');
        
        const html = `
            <div class="row">
                ${rules.map((rule, index) => `
                    <div class="col-md-6 mb-3">
                        <div class="card h-100">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i class="fas fa-arrow-right"></i> Quy tắc ${index + 1}</h6>
                            </div>
                            <div class="card-body">
                                <p><strong>Mô tả:</strong> ${rule.description}</p>
                                <div class="border-left border-warning pl-3">
                                    <small class="text-muted">
                                        <strong>Tiếng Việt:</strong> ${rule.example.vietnamese}<br>
                                        <strong>Ngôn ngữ ký hiệu:</strong> ${rule.example.sign_language}
                                    </small>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayKeyDifferences(differences) {
        const container = document.getElementById('keyDifferencesInfo');
        
        const html = `
            <div class="accordion" id="differencesAccordion">
                ${differences.map((diff, index) => `
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="heading${index}">
                            <button class="accordion-button ${index === 0 ? '' : 'collapsed'}" type="button" 
                                    data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                                <i class="fas fa-chevron-right me-2"></i>
                                ${diff.aspect}
                            </button>
                        </h2>
                        <div id="collapse${index}" class="accordion-collapse collapse ${index === 0 ? 'show' : ''}" 
                             data-bs-parent="#differencesAccordion">
                            <div class="accordion-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6 class="text-primary">Tiếng Việt</h6>
                                        <p>${diff.vietnamese}</p>
                                    </div>
                                    <div class="col-md-6">
                                        <h6 class="text-success">Ngôn ngữ Ký hiệu</h6>
                                        <p>${diff.sign_language}</p>
                                    </div>
                                </div>
                                <div class="mt-3 p-3 bg-light rounded">
                                    <h6 class="text-info"><i class="fas fa-lightbulb"></i> Ý nghĩa</h6>
                                    <p class="mb-0">${diff.implication}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        
        container.innerHTML = html;
    }

    showError(message) {
        const containers = [
            'vietnameseGrammarInfo',
            'signLanguageGrammarInfo', 
            'conversionRulesInfo',
            'keyDifferencesInfo'
        ];
        
        containers.forEach(containerId => {
            const container = document.getElementById(containerId);
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>
            `;
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new GrammarComparison();
});
