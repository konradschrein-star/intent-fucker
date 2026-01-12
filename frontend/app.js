/**
 * Keyword Classifier Frontend Application
 * 
 * This file controls everything you see and interact with in the browser!
 * It handles:
 * - Showing/hiding different sections
 * - Uploading files
 * - Sending data to the backend
 * - Updating progress bars
 * - Displaying results
 * 
 * Think of it as the "face" of the app that users interact with,
 * while the backend (Python) is the "brain" that does the AI work.
 */

// Where our backend server is running (change if your backend is on a different port)
const API_BASE_URL = 'http://localhost:5000/api';

// ============================================================================
// STATE VARIABLES - These store the current state of the application
// ============================================================================

// The ID of the current processing job (assigned by backend when you click "Start")
let currentJobId = null;

// Path to the uploaded CSV file (stored after successful upload)
let uploadedFilePath = null;

// List of categories users can classify keywords into
// Users can add/remove from this list in the UI
let categories = ['how-to', 'comparison', 'walkthrough', 'informational', 'transactional'];

// Default AI prompt (loaded from backend, can be edited by users)
let defaultClassificationPrompt = '';  // Combined prompt for relevance + category

// DOM Elements
const elements = {
    // Status Section
    backendStatusCard: document.getElementById('backendStatusCard'),
    backendStatus: document.getElementById('backendStatus'),
    startBackendBtn: document.getElementById('startBackendBtn'),
    ollamaStatusCard: document.getElementById('ollamaStatusCard'),
    ollamaStatus: document.getElementById('ollamaStatus'),
    ollamaStatusText: document.getElementById('ollamaStatusText'),
    showOllamaGuideBtn: document.getElementById('showOllamaGuideBtn'),
    ollamaGuide: document.getElementById('ollamaGuide'),
    closeGuideBtn: document.getElementById('closeGuideBtn'),

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
    classificationPrompt: document.getElementById('classificationPrompt'),
    resetClassificationPrompt: document.getElementById('resetClassificationPrompt'),

    // Processing
    startBtn: document.getElementById('startBtn'),
    progressContainer: document.getElementById('progressContainer'),
    progressStatus: document.getElementById('progressStatus'),
    progressPercentage: document.getElementById('progressPercentage'),
    progressCount: document.getElementById('progressCount'),
    timeEstimate: document.getElementById('timeEstimate'),
    progressFill: document.getElementById('progressFill'),
    consoleOutput: document.getElementById('consoleOutput'),
    consoleBadge: document.getElementById('consoleBadge'),

    // Results
    resultsSection: document.getElementById('resultsSection'),
    statTotal: document.getElementById('statTotal'),
    statAccepted: document.getElementById('statAccepted'),
    statRejected: document.getElementById('statRejected'),
    statRate: document.getElementById('statRate'),
    categoryBreakdown: document.getElementById('categoryBreakdown'),
    categoryBars: document.getElementById('categoryBars'),
    downloadAccepted: document.getElementById('downloadAccepted'),
    downloadRejected: document.getElementById('downloadRejected'),

    // Processing Console
    consoleSection: document.getElementById('consoleSection'),
    consoleOutput: document.getElementById('consoleOutput'),
    consoleBadge: document.getElementById('consoleBadge'),
    progressFill: document.getElementById('progressFill'),
    progressPercentage: document.getElementById('progressPercentage'),
    progressCount: document.getElementById('progressCount'),
    progressStatus: document.getElementById('progressStatus'),
    timeEstimate: document.getElementById('timeEstimate')
};

// ============================================================================
// INITIALIZATION - This runs when the page first loads
// ============================================================================

async function init() {
    try {
        // 1. Check system status (backend + Ollama)
        // This function is defined in app-enhanced.js
        if (typeof checkSystemStatus === 'function') {
            await checkSystemStatus();
        } else {
            console.error('checkSystemStatus not found - app-enhanced.js may not be loaded');
        }

        // 2. Setup Ollama installation guide handlers
        if (typeof setupOllamaGuide === 'function') {
            setupOllamaGuide();
        }

        // 3. Load default settings from the backend 
        await loadSettings();

        // 4. Setup all button clicks, file uploads, etc.
        setupEventListeners();

        // 5. Refresh status every 30 seconds
        if (typeof checkSystemStatus === 'function') {
            setInterval(checkSystemStatus, 30000);
        }
    } catch (error) {
        console.error('Error during initialization:', error);
        alert('⚠️ Failed to initialize the application.\n\nPlease refresh the page or check the console for details.');
    }
}

// Load settings
async function loadSettings() {
    try {
        const response = await fetch(`${API_BASE_URL}/settings`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        // Load confidence threshold
        if (data.confidence_threshold) {
            elements.confidenceSlider.value = data.confidence_threshold;
            elements.confidenceValue.textContent = data.confidence_threshold;
        }

        // Load categories
        if (data.categories && Array.isArray(data.categories)) {
            categories = data.categories;
            renderCategories();
        }

        // Load prompts
        // Load combined classification prompt
        if (data.classification_prompt) {
            defaultClassificationPrompt = data.classification_prompt;
            elements.classificationPrompt.value = data.classification_prompt;
        }

        console.log('✅ Settings loaded successfully');
    } catch (error) {
        console.error('Error loading settings:', error);
        console.warn('Using default settings');

        // Use fallback defaults if backend is unavailable
        elements.confidenceSlider.value = 75;
        elements.confidenceValue.textContent = '75';
        renderCategories(); // Use the default categories already set

        // Don't alert here - backend might just be starting up
        // User will see the issue when they try to process
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
    elements.resetClassificationPrompt.addEventListener('click', () => {
        elements.classificationPrompt.value = defaultClassificationPrompt;
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
    // Validate file type
    if (!file.name.endsWith('.csv')) {
        alert('⚠️ Invalid file type\n\nPlease upload a CSV file (.csv extension)');
        return;
    }

    // Validate file size (50MB limit)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    if (file.size > maxSize) {
        alert(`⚠️ File too large\n\nMaximum file size: 50MB\nYour file: ${(file.size / 1024 / 1024).toFixed(2)}MB`);
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.success) {
            uploadedFilePath = data.filepath;
            elements.fileName.textContent = file.name;
            elements.fileCount.textContent = `${data.keyword_count} keywords`;
            elements.uploadZone.style.display = 'none';
            elements.fileInfo.style.display = 'flex';
        } else {
            throw new Error(data.error || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload error:', error);

        let errorMessage = 'Failed to upload file:\n\n';

        if (error.message.includes('Failed to fetch')) {
            errorMessage += '❌ Cannot connect to backend server\n\n';
            errorMessage += 'Make sure the backend is running.';
        } else if (error.message.includes('Missing required columns')) {
            errorMessage += '❌ Invalid CSV format\n\n';
            errorMessage += 'Your CSV must have these columns:\n';
            errorMessage += '• title\n';
            errorMessage += '• views\n';
            errorMessage += '• views_per_year';
        } else {
            errorMessage += error.message;
        }

        alert(errorMessage);
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
        alert('⚠️ Category already exists\n\nTry a different name.');
        return;
    }

    categories.push(newCategory);
    renderCategories();
    elements.newCategoryInput.value = '';
}

function removeCategory(category) {
    if (categories.length <= 1) {
        alert('⚠️ Cannot remove last category\n\nYou must have at least one category.');
        return;
    }

    categories = categories.filter(c => c !== category);
    renderCategories();
}

// Processing
async function startProcessing() {
    const topic = elements.topicInput.value.trim();

    // Validate topic
    if (!topic) {
        alert('⚠️ Please enter a topic\n\nExample: "Ys video game series"');
        elements.topicInput.focus();
        return;
    }

    // Check input source
    const hasFile = uploadedFilePath !== null;
    const hasManualInput = elements.manualInput.value.trim() !== '';

    if (!hasFile && !hasManualInput) {
        alert('⚠️ Please provide keywords\n\nYou can either:\n• Upload a CSV file, or\n• Enter keywords manually in the "Manual Input" tab');
        // Validate categories exist
        if (categories.length === 0) {
            alert('⚠️ You must have at least one category\n\nPlease add a category in the settings.');
            return;
        }

        // Reset UI for new processing
        elements.resultsSection.style.display = 'none';

        // Show and reset processing console
        elements.consoleSection.style.display = 'block';
        if (window.resetConsole) {
            window.resetConsole();
        }

        // Reset progress
        elements.progressPercentage.textContent = '0%';
        elements.progressCount.textContent = '0 / 0';
        elements.progressFill.style.width = '0%';
        elements.progressStatus.textContent = 'Starting...';
        elements.timeEstimate.textContent = 'Calculating...';

        // Disable start button during processing
        elements.startBtn.disabled = true;
        elements.startBtn.textContent = 'Processing...';

        // Prepare request data
        const requestData = {
            topic,
            confidence_threshold: parseInt(elements.confidenceSlider.value),
            categories,
            classification_prompt: elements.classificationPrompt.value
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

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success) {
                currentJobId = data.job_id;

                // Reset console
                if (typeof resetConsole === 'function') {
                    resetConsole();
                }

                // Show progress
                elements.startBtn.disabled = true;
                elements.progressContainer.style.display = 'block';
                elements.resultsSection.style.display = 'none';

                // Start polling with enhanced version
                if (typeof pollProgressEnhanced === 'function') {
                    pollProgressEnhanced();
                } else {
                    // Fallback to basic polling
                    console.warn('Enhanced polling not available, using basic polling');
                    pollProgress();
                }
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Error starting processing:', error);

            let errorMessage = 'Failed to start processing:\n\n';

            if (error.message.includes('Failed to fetch')) {
                errorMessage += '❌ Cannot connect to backend server\n\n';
                errorMessage += 'Make sure the backend is running:\n';
                errorMessage += '1. Open terminal\n';
                errorMessage += '2. cd backend\n';
                errorMessage += '3. python app.py';
            } else {
                errorMessage += error.message;
            }

            alert(errorMessage);
        }
    }

    async function pollProgress() {
        if (!currentJobId) return;

        try {
            const response = await fetch(`${API_BASE_URL}/progress/${currentJobId}`);
            return;
        }

    // Validate categories exist
    if (categories.length === 0) {
            alert('⚠️ You must have at least one category\n\nPlease add a category in the settings.');
            return;
        }

        // Reset UI for new processing
        elements.resultsSection.style.display = 'none';

        // Show and reset processing console
        elements.consoleSection.style.display = 'block';
        if (window.resetConsole) {
            window.resetConsole();
        }

        // Reset progress
        elements.progressPercentage.textContent = '0%';
        elements.progressCount.textContent = '0 / 0';
        elements.progressFill.style.width = '0%';
        elements.progressStatus.textContent = 'Starting...';
        elements.timeEstimate.textContent = 'Calculating...';

        // Disable start button during processing
        elements.startBtn.disabled = true;
        elements.startBtn.textContent = 'Processing...';

        // Prepare request data
        const requestData = {
            topic,
            confidence_threshold: parseInt(elements.confidenceSlider.value),
            categories,
            classification_prompt: elements.classificationPrompt.value
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

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success) {
                currentJobId = data.job_id;

                // Reset console
                if (typeof resetConsole === 'function') {
                    resetConsole();
                }

                // Show progress
                elements.startBtn.disabled = true;
                elements.progressContainer.style.display = 'block';
                elements.resultsSection.style.display = 'none';

                // Start polling with enhanced version
                if (typeof pollProgressEnhanced === 'function') {
                    pollProgressEnhanced();
                } else {
                    // Fallback to basic polling
                    console.warn('Enhanced polling not available, using basic polling');
                    pollProgress();
                }
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
        } catch (error) {
            console.error('Error starting processing:', error);

            let errorMessage = 'Failed to start processing:\n\n';

            if (error.message.includes('Failed to fetch')) {
                errorMessage += '❌ Cannot connect to backend server\n\n';
                errorMessage += 'Make sure the backend is running:\n';
                errorMessage += '1. Open terminal\n';
                errorMessage += '2. cd backend\n';
                errorMessage += '3. python app.py';
            } else {
                errorMessage += error.message;
            }

            alert(errorMessage);
        }
    }

    function pollProgress() {
        // Use enhanced polling if available (shows live console + progress)
        if (window.pollProgressEnhanced) {
            window.pollProgressEnhanced();
            return;
        }

        // Fallback to basic polling
        if (!currentJobId) return;

        fetch(`${API_BASE_URL}/progress/${currentJobId}`)
            .then(response => response.json())
            .then(data => {
                console.log('Progress:', data);

                if (data.status === 'completed') {
                    loadResults();
                } else if (data.status === 'failed') {
                    alert('Processing failed');
                    resetProcessing();
                } else {
                    setTimeout(pollProgress, 500);
                }
            })
            .catch(error => {
                console.error('Error polling progress:', error);
                setTimeout(pollProgress, 1000);
                const data = await response.json();

                if (data.status === 'completed') {
                    displayResults(data);
                    resetProcessing();
                }
            } catch (error) {
                console.error('Error loading results:', error);
                alert('❌ Error loading results\n\nPlease try refreshing the page.');
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
