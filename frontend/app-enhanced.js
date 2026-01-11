// Additional functionality for enhanced features
// This extends app.js with status monitoring, Ollama guide, and live console

// ============================================================================
// STATUS MONITOR ING - Check backend and Ollama status
// ============================================================================

async function checkSystemStatus() {
    // Check backend status
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        // Update backend status
        elements.backendStatus.textContent = '✅ Online';
        elements.backendStatusCard.classList.add('online');
        elements.backendStatusCard.classList.remove('offline');

        // Update Ollama status
        if (data.ollama_available) {
            const models = data.models.join(', ') || 'No models';
            elements.ollamaStatusText.textContent = `✅ Online (${models})`;
            elements.ollamaStatusCard.classList.add('online');
            elements.ollamaStatusCard.classList.remove('offline');
            elements.showOllamaGuideBtn.style.display = 'none';

            // Also update header status
            elements.ollamaStatus.classList.add('online');
            elements.ollamaStatus.classList.remove('offline');
            elements.ollamaStatus.innerHTML = `
                <div class="status-dot"></div>
                <span>Ollama Online</span>
            `;
        } else {
            elements.ollamaStatusText.textContent = '❌ Offline - Model not running';
            elements.ollamaStatusCard.classList.add('offline');
            elements.ollamaStatusCard.classList.remove('online');
            elements.showOllamaGuideBtn.style.display = 'block';

            // Also update header status
            elements.ollamaStatus.classList.add('offline');
            elements.ollamaStatus.classList.remove('online');
            elements.ollamaStatus.innerHTML = `
                <div class="status-dot"></div>
                <span>Ollama Offline</span>
            `;
        }
    } catch (error) {
        // Backend is offline
        elements.backendStatus.textContent = '❌ Offline';
        elements.backendStatusCard.classList.add('offline');
        elements.backendStatusCard.classList.remove('online');

        elements.ollamaStatusText.textContent = '❓ Unknown (Backend offline)';
        elements.ollamaStatusCard.classList.add('offline');
        elements.ollamaStatusCard.classList.remove('online');

        // Header status
        elements.ollamaStatus.classList.add('offline');
        elements.ollamaStatus.classList.remove('online');
        elements.ollamaStatus.innerHTML = `
            <div class="status-dot"></div>
            <span>Backend Offline</span>
        `;
    }
}

// ============================================================================
// OLLAMA INSTALLATION GUIDE
// ============================================================================

function setupOllamaGuide() {
    // Show guide when button clicked
    elements.showOllamaGuideBtn.addEventListener('click', () => {
        elements.ollamaGuide.style.display = 'block';
        elements.ollamaGuide.scrollIntoView({ behavior: 'smooth' });
    });

    // Hide guide when close button clicked
    elements.closeGuideBtn.addEventListener('click', () => {
        elements.ollamaGuide.style.display = 'none';
    });
}

// ============================================================================
// LIVE CONSOLE - Show real-time keyword processing
// ============================================================================

function addConsoleMessage(message, type = 'info') {
    const consoleLine = document.createElement('div');
    consoleLine.className = `console-line console-${type}`;
    consoleLine.textContent = message;

    elements.consoleOutput.appendChild(consoleLine);

    // Auto-scroll to bottom
    elements.consoleOutput.scrollTop = elements.consoleOutput.scrollHeight;

    // Keep only last 50 messages to avoid memory issues
    const lines = elements.consoleOutput.querySelectorAll('.console-line');
    if (lines.length > 50) {
        lines[0].remove();
    }
}

function resetConsole() {
    elements.consoleOutput.innerHTML = '<div class="console-line console-info">🚀 Starting classification...</div>';
    elements.consoleBadge.textContent = '0 processed';
}

// ============================================================================
// TIME ESTIMATION - Calculate remaining time
// ============================================================================

function formatTime(seconds) {
    if (!seconds || seconds < 0) return 'Calculating...';

    if (seconds < 60) {
        return `~${Math.round(seconds)}s remaining`;
    } else if (seconds < 3600) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.round(seconds % 60);
        return `~${mins}m ${secs}s remaining`;
    } else {
        const hours = Math.floor(seconds / 3600);
        const mins = Math.round((seconds % 3600) / 60);
        return `~${hours}h ${mins}m remaining`;
    }
}

// ============================================================================
// ENHANCED PROGRESS POLLING
// ============================================================================

async function pollProgressEnhanced() {
    if (!currentJobId) return;

    try {
        const response = await fetch(`${API_BASE_URL}/progress/${currentJobId}`);
        const data = await response.json();

        // Update progress bar
        const percentage = data.percentage || 0;
        elements.progressPercentage.textContent = `${percentage.toFixed(1)}%`;
        elements.progressCount.textContent = `${data.progress} / ${data.total}`;
        elements.progressFill.style.width = `${percentage}%`;

        // Update time estimation
        if (data.time_remaining) {
            elements.timeEstimate.textContent = formatTime(data.time_remaining);
        } else {
            elements.timeEstimate.textContent = 'Estimating time...';
        }

        // Update console with latest keyword result
        if (data.current_result) {
            const result = data.current_result;
            const icon = result.accepted ? '✅' : '❌';
            const status = result.accepted ? 'ACCEPTED' : 'REJECTED';
            const score = result.score;
            const category = result.category;

            const message = `${icon} [${status}] "${result.keyword}" (Score: ${score}%, Category: ${category})`;
            const type = result.accepted ? 'success' : 'error';

            addConsoleMessage(message, type);
        }

        // Update console badge
        elements.consoleBadge.textContent = `${data.progress} processed`;

        // Check if completed
        if (data.status === 'completed') {
            addConsoleMessage('🎉 Classification complete!', 'success');
            await loadResults();
        } else if (data.status === 'failed') {
            addConsoleMessage('❌ Processing failed!', 'error');
            alert('Processing failed');
            resetProcessing();
        } else {
            // Continue polling
            setTimeout(pollProgressEnhanced, 500);
        }
    } catch (error) {
        console.error('Error polling progress:', error);
        setTimeout(pollProgressEnhanced, 1000);
    }
}

// Export functions to be used from main app.js
window.checkSystemStatus = checkSystemStatus;
window.setupOllamaGuide = setupOllamaGuide;
window.resetConsole = resetConsole;
window.pollProgressEnhanced = pollProgressEnhanced;
