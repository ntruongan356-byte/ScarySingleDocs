/**
 * Consolidated Widget JavaScript - ScarySingleDocs
 * Handles all dynamic UI interactions for the refactored notebook interface.
 */

// === INITIALIZATION ===
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing ScarySingleDocs UI...');
    initializeAll();
    console.log('All systems initialized successfully!');
});

function initializeAll() {
    initializeTopTabs();
    initializeModelItems();
    initializeDrawer();
    initializeBottomTabs();
    initializeEmpowerment();
    initializeUtilityButtons();
}

// === UI COMPONENT INITIALIZERS ===

// 1. Top-level download tabs (Models, VAE, etc.)
function initializeTopTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.tab;
            
            // Deactivate all
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Activate clicked
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab + '-content');
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// 2. Selectable model items
function initializeModelItems() {
    const modelItems = document.querySelectorAll('.model-item');
    modelItems.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
}

// 3. Advanced Options Drawer
function initializeDrawer() {
    const drawerToggle = document.getElementById('drawer-toggle');
    const drawerSections = document.getElementById('drawer-sections');
    if (!drawerToggle || !drawerSections) return;

    let isOpen = false;

    drawerToggle.addEventListener('click', function() {
        isOpen = !isOpen;
        
        if (isOpen) {
            drawerSections.classList.remove('hidden');
            drawerSections.classList.add('shown');
            drawerToggle.classList.add('expanded');
            drawerToggle.querySelector('.drawer-toggle-text').textContent = 'Hide Advanced Options';
        } else {
            drawerSections.classList.remove('shown');
            drawerSections.classList.add('hidden');
            drawerToggle.classList.remove('expanded');
            drawerToggle.querySelector('.drawer-toggle-text').textContent = 'Advanced Options';
        }
    });
}

// 4. Tabs within the Advanced Drawer (Custom Download, etc.)
function initializeBottomTabs() {
    const bottomTabButtons = document.querySelectorAll('.bottom-tab-button');
    const bottomTabContents = document.querySelectorAll('.bottom-tab-content');
    if (bottomTabButtons.length === 0) return;

    bottomTabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.dataset.bottomTab;
            
            // Deactivate all
            bottomTabButtons.forEach(btn => btn.classList.remove('active'));
            bottomTabContents.forEach(content => content.classList.remove('active'));
            
            // Activate clicked
            this.classList.add('active');
            const targetContent = document.getElementById(targetTab + '-content');
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// 5. Empowerment (Text Area vs. Individual Fields) Toggle
function initializeEmpowerment() {
    const empowermentToggle = document.getElementById('empowerment');
    const textareaContainer = document.getElementById('empowerment-textarea-container');
    const individualFields = document.getElementById('individual-fields');
    if (!empowermentToggle || !textareaContainer || !individualFields) return;

    empowermentToggle.addEventListener('change', function() {
        if (this.checked) {
            textareaContainer.style.display = 'block';
            individualFields.style.display = 'none';
        } else {
            textareaContainer.style.display = 'none';
            individualFields.style.display = 'block';
        }
    });
}

// 6. Utility Buttons (Export/Import/GDrive)
function initializeUtilityButtons() {
    // These will likely trigger Python callbacks, so we just need placeholders
    // The actual logic is in the Python script.
    const gdriveButton = document.querySelector('.utility-button[title="Google Drive"]');
    const exportButton = document.querySelector('.utility-button[title="Export"]');
    const importButton = document.querySelector('.utility-button[title="Import"]');

    const saveButton = document.querySelector('.button_save');
    if (saveButton) {
        saveButton.addEventListener('click', () => {
            if (typeof google !== 'undefined' && google.colab && google.colab.kernel) {
                google.colab.kernel.invokeFunction('notebook.save_data_from_js', [], {});
            }
        });
    }

    if (importButton) {
        importButton.addEventListener('click', () => {
            if (typeof google !== 'undefined' && google.colab && google.colab.kernel) {
                google.colab.kernel.invokeFunction('importSettingsFromJS', [], {});
            }
        });
    }
}


// === PYTHON COMMUNICATION & HELPERS ===

// Function to be called from Python to download JSON
function downloadJson(data, filename = 'widget_settings.json') {
    try {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showNotification('Settings exported successfully!', 'success');
    } catch (error) {
        showNotification(`Export failed: ${error.message}`, 'error');
    }
}

// Function to be called from Python to open file picker
function openFilePicker() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;
        try {
            const text = await file.text();
            const jsonData = JSON.parse(text);
            if (typeof google !== 'undefined' && google.colab && google.colab.kernel) {
                google.colab.kernel.invokeFunction('importSettingsFromJS', [jsonData], {});
            }
        } catch (err) {
            showNotification(`Import failed: ${err.message}`, 'error');
        }
    };
    input.click();
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notificationPopup = document.querySelector('.notification-popup');
    if (!notificationPopup) return;

    const iconMap = {
        'success': '✅',
        'error': '❌',
        'info': '💡',
        'warning': '⚠️'
    };
    const icon = iconMap[type] || '💡';

    notificationPopup.innerHTML = `
        <div class="notification ${type}">
            <span class="notification-icon">${icon}</span>
            <span class="notification-text">${message}</span>
        </div>
    `;

    notificationPopup.classList.remove('hidden');
    notificationPopup.classList.add('visible');

    setTimeout(() => {
        notificationPopup.classList.remove('visible');
        notificationPopup.classList.add('hidden');
    }, duration);
}