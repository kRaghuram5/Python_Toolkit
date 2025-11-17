// Global variables
let selectedOperation = null;
let selectedFiles = [];
let operations = [];

// Icons mapping for operations
const operationIcons = {
    'pdf_to_word': 'fa-file-word',
    'pdf_to_text': 'fa-file-alt',
    'pdf_to_images': 'fa-images',
    'word_to_pdf': 'fa-file-pdf',
    'text_to_pdf': 'fa-file-pdf',
    'images_to_pdf': 'fa-file-pdf',
    'extract_images': 'fa-image',
    'reverse_pdf': 'fa-exchange-alt',
    'merge_pdfs': 'fa-layer-group'
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadOperations();
    setupEventListeners();
});

// Load available operations from the API
async function loadOperations() {
    try {
        const response = await fetch('/api/operations');
        operations = await response.json();
        displayOperations(operations);
    } catch (error) {
        console.error('Error loading operations:', error);
        showError('Failed to load operations. Please refresh the page.');
    }
}

// Display operations in the grid
function displayOperations(operations) {
    const grid = document.getElementById('operationsGrid');
    grid.innerHTML = '';

    operations.forEach(operation => {
        const card = document.createElement('div');
        card.className = 'operation-card';
        card.onclick = () => selectOperation(operation);

        const icon = operationIcons[operation.id] || 'fa-file';
        const badge = operation.multiple ? 
            '<span class="operation-badge"><i class="fas fa-layer-group"></i> Multiple Files</span>' :
            '<span class="operation-badge"><i class="fas fa-file"></i> Single File</span>';

        card.innerHTML = `
            <div class="operation-icon">
                <i class="fas ${icon}"></i>
            </div>
            <h3>${operation.name}</h3>
            <p>${operation.description}</p>
            <div>${badge}</div>
        `;

        grid.appendChild(card);
    });
}

// Select an operation
function selectOperation(operation) {
    selectedOperation = operation;
    selectedFiles = [];

    // Update UI
    document.querySelector('.operations-section').style.display = 'none';
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('operationTitle').textContent = operation.name;

    // Update file input attributes
    const fileInput = document.getElementById('fileInput');
    fileInput.multiple = operation.multiple;
    
    // Update hint text
    const hint = document.getElementById('uploadHint');
    hint.textContent = `Accepts: ${operation.accepts} | Produces: ${operation.produces}`;
    
    // Update drag area text
    const uploadArea = document.querySelector('.upload-area h3');
    uploadArea.textContent = operation.multiple ? 
        'Drag & Drop Your Files Here (Multiple files allowed)' : 
        'Drag & Drop Your File Here';
}

// Setup event listeners
function setupEventListeners() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Drag and drop events
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    // File input change event
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

// Handle selected files
function handleFiles(files) {
    if (!selectedOperation) return;

    if (!selectedOperation.multiple && files.length > 1) {
        showError('This operation only accepts a single file.');
        return;
    }

    selectedFiles = Array.from(files);
    displayFilesPreview();
    updateConvertButton();
}

// Display files preview
function displayFilesPreview() {
    const preview = document.getElementById('filesPreview');
    preview.innerHTML = '';

    if (selectedFiles.length === 0) {
        return;
    }

    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';

        const fileIcon = getFileIcon(file.name);
        const fileSize = formatFileSize(file.size);

        fileItem.innerHTML = `
            <div class="file-info">
                <div class="file-icon">
                    <i class="fas ${fileIcon}"></i>
                </div>
                <div class="file-details">
                    <h4>${file.name}</h4>
                    <p>${fileSize}</p>
                </div>
            </div>
            <button class="btn-remove" onclick="removeFile(${index})">
                <i class="fas fa-times"></i> Remove
            </button>
        `;

        preview.appendChild(fileItem);
    });
}

// Get file icon based on extension
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const iconMap = {
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word',
        'docx': 'fa-file-word',
        'txt': 'fa-file-alt',
        'png': 'fa-file-image',
        'jpg': 'fa-file-image',
        'jpeg': 'fa-file-image',
        'bmp': 'fa-file-image',
        'gif': 'fa-file-image'
    };
    return iconMap[ext] || 'fa-file';
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Remove file from selection
function removeFile(index) {
    selectedFiles.splice(index, 1);
    displayFilesPreview();
    updateConvertButton();
}

// Update convert button state
function updateConvertButton() {
    const convertBtn = document.getElementById('convertBtn');
    convertBtn.disabled = selectedFiles.length === 0;
}

// Convert files
async function convertFiles() {
    if (selectedFiles.length === 0) return;

    // Hide upload section, show progress
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'block';

    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    formData.append('operation', selectedOperation.id);

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showSuccess(result.download_url);
        } else {
            showError(result.error || 'Conversion failed. Please try again.');
        }
    } catch (error) {
        console.error('Conversion error:', error);
        showError('An error occurred during conversion. Please try again.');
    }
}

// Show success result
function showSuccess(downloadUrl) {
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'block';

    const resultIcon = document.getElementById('resultIcon');
    resultIcon.className = 'result-icon success';
    resultIcon.innerHTML = '<i class="fas fa-check-circle"></i>';

    document.getElementById('resultTitle').textContent = 'Conversion Successful!';
    document.getElementById('resultMessage').textContent = 'Your file is ready to download.';

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.href = downloadUrl;
    downloadBtn.style.display = 'inline-block';
}

// Show error result
function showError(message) {
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'block';

    const resultIcon = document.getElementById('resultIcon');
    resultIcon.className = 'result-icon error';
    resultIcon.innerHTML = '<i class="fas fa-exclamation-circle"></i>';

    document.getElementById('resultTitle').textContent = 'Conversion Failed';
    document.getElementById('resultMessage').textContent = message;

    const downloadBtn = document.getElementById('downloadBtn');
    downloadBtn.style.display = 'none';
}

// Reset operation and return to main screen
function resetOperation() {
    selectedOperation = null;
    selectedFiles = [];

    // Reset file input
    document.getElementById('fileInput').value = '';

    // Hide all sections except operations
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'none';
    document.getElementById('resultSection').style.display = 'none';
    document.querySelector('.operations-section').style.display = 'block';

    // Clear files preview
    document.getElementById('filesPreview').innerHTML = '';
}

// Show notification
function showNotification(message, type = 'info') {
    // You can implement a toast notification system here
    console.log(`${type.toUpperCase()}: ${message}`);
}
