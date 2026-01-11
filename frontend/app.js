/**
 * Keyword Classifier Frontend Application
 * Handles UI interactions and API communication
 */

const API_BASE_URL = 'http://localhost:5000/api';

// State
let currentJobId = null;
let uploadedFilePath = null;
let categories = ['how-to', 'comparison', 'walkthrough', 'informational', 'transactional'];
let defaultRelevancePrompt = '';
let defaultCategoryPrompt = '';

// DOM Elements
const elements = {
    // Status
    ollamaStatus: document.getElementById('ollamaStatus'),

    // Input
    topicInput: document.getElementById('topicInput'),
    fileInput: document.getElementById('fileInput'),
    uploadZone: document.getElementById('uploadZone'),
    fileInfo: document.getElementById('fileInfo'),
    fileName: document.getElementById('fileName'),
    fileCount: document.getElementById('fileCount'),
    removeFileBtn: document.getElementById('removeFile'),
    manualInput: document.getElementById('manualInput'),

    // Tabs
    tabButtons: document.querySelectorAll('.tab-button'),
    uploadTab: document.getElementById('uploadTab'),
    manualTab: document.getElementById('manualTab'),

    // Settings
    settingsToggle: document.getElementById('settingsToggle'),
    settingsContent: document.getElementById('settingsContent'),
    confidenceSlider: document.getElementById('confidenceSlider'),
    confidenceValue: document.getElementById('confidenceValue'),
    categoryList: document.getElementById('categoryList'),
    newCategoryInput: document.getElementById('newCategoryInput'),
    addCategoryBtn: document.getElementById('addCategoryBtn'),
    relevancePrompt: document.getElementById('relevancePrompt'),
    categoryPrompt: document.getElementById('categoryPrompt'),
    resetRelevancePrompt: document.getElementById('resetRelevancePrompt'),
    resetCategoryPrompt: document.getElementById('resetCategoryPrompt'),

    // Processing
    startBtn: document.getElementById('startBtn'),
    progressContainer: document.getElementById('progressContainer'),
    progressStatus: document.getElementById('progressStatus'),
    progressPercentage: document.getElementById('progressPercentage'),
    progressCount: document.getElementById('progressCount'),
    currentKeyword: document.getElementById('currentKeyword'),
    progressFill: document.getElementById('progressFill'),

    // Results
    resultsSection: document.getElementById('resultsSection'),
    statTotal: document.getElementById('statTotal'),
    statAccepted: document.getElementById('statAccepted'),
    statRejected: document.getElementById('statRejected'),
    statRate: document.getElementById('statRate'),
    categoryBreakdown: document.getElementById('categoryBreakdown'),
    categoryBars: document.getElementById('categoryBars'),
    downloadAccepted: document.getElementById('downloadAccepted'),
    downloadRejected: document.getElementById('downloadRejected')
};

// Initialize
async function init() {
    await checkOllamaStatus();
    await loadSettings();
    setupEventListeners();
}

// Check Ollama status
async function checkOllamaStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.ollama_available) {
            elements.ollamaStatus.classList.add('online');
            elements.ollamaStatus.innerHTML = `
                <div class="status-dot"></div>
                <span>Ollama Online (${data.models.join(', ') || 'No models'})</span>
            `;
        } else {
            elements.ollamaStatus.classList.add('offline');
            elements.ollamaStatus.innerHTML = `
                <div class="status-dot"></div>
                <span>Ollama Offline</span>
            `;
        }
    } catch (error) {
        elements.ollamaStatus.classList.add('offline');
        elements.ollamaStatus.innerHTML = `
            <div class="status-dot"></div>
            <span>Backend Offline</span>
        `;
    }
}

// Load settings
async function loadSettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/settings`);
        const data = await response.json();

        elements.confidenceSlider.value = data.confidence_threshold;
        elements.confidenceValue.textContent = data.confidence_threshold;

        categories = data.categories;
        renderCategories();

        defaultRelevancePrompt = data.relevance_prompt;
        defaultCategoryPrompt = data.category_prompt;
        elements.relevancePrompt.value = data.relevance_prompt;
        elements.categoryPrompt.value = data.category_prompt;
    } catch (error) {
        console.error('Error loading settings:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    // Tabs
    elements.tabButtons.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.dataset.tab));
    });

    // File upload
    elements.uploadZone.addEventListener('click', () => elements.fileInput.click());
    elements.uploadZone.addEventListener('dragover', handleDragOver);
    elements.uploadZone.addEventListener('dragleave', handleDragLeave);
    elements.uploadZone.addEventListener('drop', handleDrop);
    elements.fileInput.addEventListener('change', handleFileSelect);
    elements.removeFileBtn.addEventListener('click', removeFile);

    // Settings
    elements.settingsToggle.addEventListener('click', toggleSettings);
    elements.confidenceSlider.addEventListener('input', updateConfidenceValue);
    elements.addCategoryBtn.addEventListener('click', addCategory);
    elements.newCategoryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addCategory();
    });
    elements.resetRelevancePrompt.addEventListener('click', () => {
        elements.relevancePrompt.value = defaultRelevancePrompt;
    });
    elements.resetCategoryPrompt.addEventListener('click', () => {
        elements.categoryPrompt.value = defaultCategoryPrompt;
    });

    // Processing
    elements.startBtn.addEventListener('click', startProcessing);
}

// Tab switching
function switchTab(tab) {
    elements.tabButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });

    elements.uploadTab.classList.toggle('active', tab === 'upload');
    elements.manualTab.classList.toggle('active', tab === 'manual');
}

// File upload handlers
function handleDragOver(e) {
    e.preventDefault();
    elements.uploadZone.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadZone.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

async function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
        alert('Please upload a CSV file');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            uploadedFilePath = data.filepath;
            elements.fileName.textContent = file.name;
            elements.fileCount.textContent = `${data.keyword_count} keywords`;
            elements.uploadZone.style.display = 'none';
            elements.fileInfo.style.display = 'flex';
        } else {
            alert(data.error || 'Upload failed');
        }
    } catch (error) {
        alert('Error uploading file: ' + error.message);
    }
}

function removeFile() {
    uploadedFilePath = null;
    elements.uploadZone.style.display = 'block';
    elements.fileInfo.style.display = 'none';
    elements.fileInput.value = '';
}

// Settings
function toggleSettings() {
    const isExpanded = elements.settingsContent.classList.toggle('expanded');
    elements.settingsToggle.classList.toggle('expanded', isExpanded);
    elements.settingsToggle.querySelector('span').textContent = isExpanded ? 'Collapse' : 'Expand';
}

function updateConfidenceValue() {
    elements.confidenceValue.textContent = elements.confidenceSlider.value;
}

function renderCategories() {
    elements.categoryList.innerHTML = categories.map(cat => `
        <span class="pill">
            ${cat}
            <button class="pill-remove" data-category="${cat}">✕</button>
        </span>
    `).join('');

    // Add event listeners to remove buttons
    document.querySelectorAll('.pill-remove').forEach(btn => {
        btn.addEventListener('click', () => removeCategory(btn.dataset.category));
    });
}

function addCategory() {
    const newCategory = elements.newCategoryInput.value.trim().toLowerCase();

    if (!newCategory) return;

    if (categories.includes(newCategory)) {
        alert('Category already exists');
        return;
    }

    categories.push(newCategory);
    renderCategories();
    elements.newCategoryInput.value = '';
}

function removeCategory(category) {
    if (categories.length <= 1) {
        alert('You must have at least one category');
        return;
    }

    categories = categories.filter(c => c !== category);
    renderCategories();
}

// Processing
async function startProcessing() {
    const topic = elements.topicInput.value.trim();

    if (!topic) {
        alert('Please enter a topic');
        return;
    }

    // Check input source
    const hasFile = uploadedFilePath !== null;
    const hasManualInput = elements.manualInput.value.trim() !== '';

    if (!hasFile && !hasManualInput) {
        alert('Please upload a CSV file or enter keywords manually');
        return;
    }

    // Prepare request
    const requestData = {
        topic,
        confidence_threshold: parseInt(elements.confidenceSlider.value),
        categories,
        relevance_prompt: elements.relevancePrompt.value,
        category_prompt: elements.categoryPrompt.value
    };

    if (hasFile) {
        requestData.filepath = uploadedFilePath;
    } else {
        requestData.manual_input = elements.manualInput.value;
    }

    try {
        // Start processing
        const response = await fetch(`${API_BASE_URL}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success) {
            currentJobId = data.job_id;

            // Show progress
            elements.startBtn.disabled = true;
            elements.progressContainer.style.display = 'block';
            elements.resultsSection.style.display = 'none';

            // Start polling
            pollProgress();
        } else {
            alert(data.error || 'Failed to start processing');
        }
    } catch (error) {
        alert('Error starting processing: ' + error.message);
    }
}

async function pollProgress() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/progress/${currentJobId}`);
        const data = await response.json();

        // Update UI
        const percentage = data.percentage || 0;
        elements.progressPercentage.textContent = `${percentage.toFixed(1)}%`;
        elements.progressCount.textContent = `${data.progress} / ${data.total}`;
        elements.currentKeyword.textContent = data.current_keyword || '';
        elements.progressFill.style.width = `${percentage}%`;

        if (data.status === 'completed') {
            // Processing complete
            await loadResults();
        } else if (data.status === 'failed') {
            alert('Processing failed');
            resetProcessing();
        } else {
            // Continue polling
            setTimeout(pollProgress, 500);
        }
    } catch (error) {
        console.error('Error polling progress:', error);
        setTimeout(pollProgress, 1000);
    }
}

async function loadResults() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/results/${currentJobId}`);
        const data = await response.json();

        if (data.status === 'completed') {
            displayResults(data);
            resetProcessing();
        }
    } catch (error) {
        console.error('Error loading results:', error);
    }
}

function displayResults(data) {
    const stats = data.statistics;

    // Update statistics
    elements.statTotal.textContent = stats.total;
    elements.statAccepted.textContent = stats.accepted;
    elements.statRejected.textContent = stats.rejected;
    elements.statRate.textContent = `${stats.acceptance_rate}%`;

    // Category breakdown
    const categoryBreakdown = stats.category_breakdown;
    const maxCount = Math.max(...Object.values(categoryBreakdown));

    elements.categoryBars.innerHTML = Object.entries(categoryBreakdown)
        .sort((a, b) => b[1] - a[1])
        .map(([category, count]) => {
            const percentage = (count / stats.total * 100).toFixed(1);
            const width = (count / maxCount * 100);

            return `
                <div class="category-bar-item">
                    <div class="category-bar-label">${category}</div>
                    <div class="category-bar-container">
                        <div class="category-bar-fill" style="width: ${width}%">
                            ${count} (${percentage}%)
                        </div>
                    </div>
                </div>
            `;
        })
        .join('');

    // Setup download buttons
    const acceptedFileName = data.accepted_file.split('\\').pop().split('/').pop();
    const rejectedFileName = data.rejected_file.split('\\').pop().split('/').pop();

    elements.downloadAccepted.onclick = () => downloadFile(acceptedFileName);
    elements.downloadRejected.onclick = () => downloadFile(rejectedFileName);

    // Show results
    elements.resultsSection.style.display = 'block';

    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function downloadFile(filename) {
    window.open(`${API_BASE_URL}/download/${filename}`, '_blank');
}

function resetProcessing() {
    elements.startBtn.disabled = false;
    elements.progressContainer.style.display = 'none';
    elements.progressFill.style.width = '0%';
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
