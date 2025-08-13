/**
 * Enhanced Widget JavaScript - ScarySingleDocs
 * Sophisticated interaction handling for cloud GPU notebook environments
 */

// === CORE FUNCTIONALITY ===

// Toggle container visibility with elegant animations
function toggleContainer() {
    const SHOW_CLASS = 'showed';
    const elements = {
        downloadContainer: document.querySelector('.container_cdl'),
        info: document.querySelector('.info'),
        empowerment: document.querySelector('.empowerment')
    };

    if (!elements.downloadContainer) return;

    // Enhanced animation with callbacks
    elements.downloadContainer.classList.toggle('expanded');
    elements.info?.classList.toggle(SHOW_CLASS);
    elements.empowerment?.classList.toggle(SHOW_CLASS);

    // Add visual feedback
    const isExpanded = elements.downloadContainer.classList.contains('expanded');
    if (isExpanded) {
        showStatusFeedback('Custom Download expanded', 'info');
    }
}

// Enhanced JSON download with progress feedback
function downloadJson(data, filename='widget_settings.json') {
    showStatusFeedback('Preparing settings export...', 'info');
    
    try {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        showStatusFeedback('Settings exported successfully!', 'success');
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    } catch (error) {
        showStatusFeedback('Export failed: ' + error.message, 'error');
    }
}

// Enhanced file picker with validation
function openFilePicker(callbackName='importSettingsFromJS') {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.style.display = 'none';

    input.onchange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        showStatusFeedback('Reading settings file...', 'info');

        try {
            // Validate file size (max 1MB for safety)
            if (file.size > 1024 * 1024) {
                throw new Error('File too large (max 1MB)');
            }

            const text = await file.text();
            const jsonData = JSON.parse(text);
            
            // Basic validation
            if (typeof jsonData !== 'object' || jsonData === null) {
                throw new Error('Invalid JSON structure');
            }

            google.colab.kernel.invokeFunction(callbackName, [jsonData], {});
        } catch (err) {
            const errorMsg = `Import failed: ${err.message}`;
            showStatusFeedback(errorMsg, 'error');
            google.colab.kernel.invokeFunction('showNotificationFromJS', [errorMsg, "error"], {});
        }
    };

    document.body.appendChild(input);
    input.click();
    document.body.removeChild(input);
}

// === PROGRESS & STATUS FEEDBACK ===

// Create and manage progress bars
function createProgressBar(container, initialValue = 0) {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container';
    
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.style.width = `${initialValue}%`;
    
    progressContainer.appendChild(progressBar);
    container.appendChild(progressContainer);
    
    return {
        update: (value) => {
            progressBar.style.width = `${Math.min(100, Math.max(0, value))}%`;
        },
        remove: () => {
            progressContainer.remove();
        }
    };
}

// Enhanced status feedback system
function showStatusFeedback(message, type = 'info', duration = 3000) {
    // Remove existing status indicators
    document.querySelectorAll('.status-indicator').forEach(el => {
        if (!el.classList.contains('persistent')) {
            el.remove();
        }
    });

    const statusIndicator = document.createElement('div');
    statusIndicator.className = `status-indicator ${type}`;
    
    // Add loading spinner for certain types
    if (type === 'downloading' || (type === 'info' && message.includes('...'))) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        statusIndicator.appendChild(spinner);
    }
    
    const textNode = document.createTextNode(message);
    statusIndicator.appendChild(textNode);
    
    // Insert into appropriate container
    const targetContainer = document.querySelector('.download-tabs-container') || document.body;
    targetContainer.appendChild(statusIndicator);
    
    // Auto-remove after duration
    if (duration > 0) {
        setTimeout(() => {
            statusIndicator.style.opacity = '0';
            setTimeout(() => statusIndicator.remove(), 300);
        }, duration);
    }
    
    return statusIndicator;
}

// Create download overlay for intensive operations
function showDownloadOverlay(title, details = '') {
    const overlay = document.createElement('div');
    overlay.className = 'download-overlay active';
    
    const spinner = document.createElement('div');
    spinner.className = 'loading-spinner';
    spinner.style.width = '40px';
    spinner.style.height = '40px';
    spinner.style.borderWidth = '4px';
    
    const info = document.createElement('div');
    info.className = 'download-info';
    
    const titleEl = document.createElement('div');
    titleEl.className = 'download-title';
    titleEl.textContent = title;
    
    const detailEl = document.createElement('div');
    detailEl.className = 'download-detail';
    detailEl.textContent = details;
    
    info.appendChild(titleEl);
    if (details) info.appendChild(detailEl);
    
    overlay.appendChild(spinner);
    overlay.appendChild(info);
    
    // Add to main container
    const mainContainer = document.querySelector('.mainContainer');
    if (mainContainer) {
        mainContainer.style.position = 'relative';
        mainContainer.appendChild(overlay);
    }
    
    return {
        updateTitle: (newTitle) => titleEl.textContent = newTitle,
        updateDetails: (newDetails) => detailEl.textContent = newDetails,
        remove: () => {
            overlay.classList.remove('active');
            setTimeout(() => overlay.remove(), 300);
        }
    };
}

// === TAB SYSTEM ENHANCEMENTS ===

// Enhanced tab switching with animations
function switchTab(targetTabId) {
    const tabs = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');
    
    // Remove active states
    tabs.forEach(tab => tab.classList.remove('active'));
    contents.forEach(content => {
        content.classList.remove('active');
        content.style.opacity = '0';
    });
    
    // Activate target tab
    const targetTab = document.querySelector(`[data-tab="${targetTabId}"]`);
    const targetContent = document.querySelector(`[data-content="${targetTabId}"]`);
    
    if (targetTab && targetContent) {
        targetTab.classList.add('active');
        setTimeout(() => {
            targetContent.classList.add('active');
            targetContent.style.opacity = '1';
        }, 150);
        
        showStatusFeedback(`${targetTabId} tab selected`, 'info', 1500);
    }
}

// === UTILITY FUNCTIONS ===

// Enhanced notification system
function hideNotification(delay = 2500) {
    setTimeout(() => {
        const popup = document.querySelector('.notification-popup');
        if (popup) {
            popup.classList.add('hidden');
            popup.classList.remove('visible');
        }
    }, delay);
}

// Debounce utility for performance
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize enhanced interactions when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Add click handlers for toggle buttons
    document.querySelectorAll('.toggle-button').forEach(button => {
        button.addEventListener('click', debounce(function(e) {
            const isActive = this.classList.toggle('active');
            showStatusFeedback(
                `${this.textContent} ${isActive ? 'selected' : 'deselected'}`,
                'info',
                1500
            );
        }, 100));
    });
    
    // Add enhanced tab functionality
    document.querySelectorAll('.tab-button').forEach(tab => {
        tab.addEventListener('click', function(e) {
            const tabId = this.textContent.toLowerCase();
            switchTab(tabId);
        });
    });
    
    console.log('Enhanced ScarySingleDocs widgets initialized');
});