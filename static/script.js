// Emotion Cipher JavaScript

class EmotionCipherApp {
    constructor() {
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        // Input elements
        this.messageInput = document.getElementById('messageInput');
        this.encryptedText = document.getElementById('encryptedText');
        this.decryptedText = document.getElementById('decryptedText');
        
        // Buttons
        this.encryptBtn = document.getElementById('encryptBtn');
        this.decryptBtn = document.getElementById('decryptBtn');
        this.copyEncryptedBtn = document.getElementById('copyEncryptedBtn');
        
        // Display elements
        this.detectedEmotion = document.getElementById('detectedEmotion');
        this.emotionBadge = document.getElementById('emotionBadge');
        this.emotionKey = document.getElementById('emotionKey');
        
        // Status elements
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorAlert = document.getElementById('errorAlert');
        this.errorMessage = document.getElementById('errorMessage');
        this.successAlert = document.getElementById('successAlert');
        this.successMessage = document.getElementById('successMessage');
    }

    bindEvents() {
        this.encryptBtn.addEventListener('click', () => this.encryptMessage());
        this.decryptBtn.addEventListener('click', () => this.decryptMessage());
        this.copyEncryptedBtn.addEventListener('click', () => this.copyToClipboard());
        
        // Allow Enter key for encryption (Ctrl+Enter)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.encryptMessage();
            }
        });
        
        // Auto-focus on message input
        this.messageInput.focus();
    }

    async encryptMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) {
            this.showError('Please enter a message to encrypt');
            return;
        }

        this.showLoading(true);
        this.hideAlerts();

        try {
            const response = await fetch('/encrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Encryption failed');
            }

            // Display results
            this.encryptedText.value = data.encrypted_text;
            this.detectedEmotion.textContent = data.detected_emotion;
            this.emotionKey.textContent = `Key: ${data.emotion_key}`;
            
            // Update emotion badge styling
            this.updateEmotionBadge(data.detected_emotion);
            
            // Clear decrypted text
            this.decryptedText.value = '';
            
            this.showResults(true);
            this.showSuccess('Message encrypted successfully!');
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async decryptMessage() {
        const encryptedText = this.encryptedText.value.trim();
        
        if (!encryptedText) {
            this.showError('Please encrypt a message first or enter encrypted text');
            return;
        }

        this.showLoading(true);
        this.hideAlerts();

        try {
            const response = await fetch('/decrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ encrypted_text: encryptedText })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Decryption failed');
            }

            // Display results
            this.decryptedText.value = data.original_message;
            this.detectedEmotion.textContent = data.detected_emotion;
            this.emotionKey.textContent = `Key: ${data.emotion_key}`;
            
            // Update emotion badge styling
            this.updateEmotionBadge(data.detected_emotion);
            
            this.showResults(true);
            this.showSuccess('Message decrypted successfully!');
            
        } catch (error) {
            this.showError(error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async copyToClipboard() {
        const text = this.encryptedText.value;
        
        if (!text) {
            this.showError('No encrypted text to copy');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            
            // Visual feedback
            const originalText = this.copyEncryptedBtn.innerHTML;
            this.copyEncryptedBtn.classList.add('copied');
            this.copyEncryptedBtn.innerHTML = '<i class="bi bi-check"></i>';
            
            setTimeout(() => {
                this.copyEncryptedBtn.classList.remove('copied');
                this.copyEncryptedBtn.innerHTML = originalText;
            }, 2000);
            
            this.showSuccess('Encrypted text copied to clipboard!');
            
        } catch (error) {
            // Fallback for older browsers
            this.encryptedText.select();
            document.execCommand('copy');
            this.showSuccess('Encrypted text copied to clipboard!');
        }
    }

    updateEmotionBadge(emotion) {
        // Remove all emotion classes
        this.emotionBadge.className = 'emotion-badge';
        
        // Add the new emotion class
        this.emotionBadge.classList.add(emotion);
        
        // Update icon based on emotion
        const iconMap = {
            'joy': 'bi-emoji-smile',
            'sadness': 'bi-emoji-frown',
            'anger': 'bi-emoji-angry',
            'fear': 'bi-emoji-dizzy',
            'surprise': 'bi-emoji-surprise',
            'neutral': 'bi-emoji-neutral'
        };
        
        const icon = iconMap[emotion] || 'bi-emoji-neutral';
        this.emotionBadge.querySelector('i').className = `bi ${icon} me-2`;
    }

    showLoading(show) {
        this.loadingIndicator.style.display = show ? 'block' : 'none';
        this.encryptBtn.disabled = show;
        this.decryptBtn.disabled = show;
    }

    showResults(show) {
        this.resultsSection.style.display = show ? 'block' : 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorAlert.style.display = 'block';
        this.successAlert.style.display = 'none';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            this.errorAlert.style.display = 'none';
        }, 5000);
    }

    showSuccess(message) {
        this.successMessage.textContent = message;
        this.successAlert.style.display = 'block';
        this.errorAlert.style.display = 'none';
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            this.successAlert.style.display = 'none';
        }, 3000);
    }

    hideAlerts() {
        this.errorAlert.style.display = 'none';
        this.successAlert.style.display = 'none';
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EmotionCipherApp();
});

// Add some utility functions
window.EmotionCipherUtils = {
    // Format encrypted text for better readability
    formatEncryptedText(text) {
        if (!text) return '';
        return text.match(/.{1,50}/g).join('\n');
    },
    
    // Validate message input
    validateMessage(message) {
        return message && message.trim().length > 0;
    },
    
    // Get emotion color for charts or visualizations
    getEmotionColor(emotion) {
        const colors = {
            'joy': '#FFD700',
            'sadness': '#4169E1',
            'anger': '#DC3545',
            'fear': '#6F42C1',
            'surprise': '#FD7E14',
            'neutral': '#6C757D'
        };
        return colors[emotion] || colors['neutral'];
    }
};
