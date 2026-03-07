from flask import Flask, render_template, request, jsonify
from emotion_model import EmotionDetector
from cipher import EmotionCipher
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize components
try:
    emotion_detector = EmotionDetector()
    cipher = EmotionCipher()
    logger.info("Emotion detection model and cipher initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {e}")
    emotion_detector = None
    cipher = None

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    """Encrypt a message with emotion detection"""
    try:
        if not cipher or not emotion_detector:
            return jsonify({
                'error': 'Server components not properly initialized'
            }), 500
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Message is required'
            }), 400
        
        message = data['message']
        
        if not message or not message.strip():
            return jsonify({
                'error': 'Message cannot be empty'
            }), 400
        
        # Detect emotion
        detected_emotion = emotion_detector.detect_emotion(message)
        logger.info(f"Detected emotion: {detected_emotion} for message: {message[:50]}...")
        
        # Encrypt the message
        encrypted_text = cipher.encrypt(message, detected_emotion)
        
        return jsonify({
            'encrypted_text': encrypted_text,
            'detected_emotion': detected_emotion,
            'emotion_key': cipher.get_emotion_key(detected_emotion)
        })
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Encryption error: {e}")
        return jsonify({
            'error': 'An unexpected error occurred during encryption'
        }), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    """Decrypt an encrypted message"""
    try:
        if not cipher:
            return jsonify({
                'error': 'Server components not properly initialized'
            }), 500
        
        data = request.get_json()
        
        if not data or 'encrypted_text' not in data:
            return jsonify({
                'error': 'Encrypted text is required'
            }), 400
        
        encrypted_text = data['encrypted_text']
        
        if not encrypted_text or not encrypted_text.strip():
            return jsonify({
                'error': 'Encrypted text cannot be empty'
            }), 400
        
        # Validate format
        if not cipher.validate_encrypted_format(encrypted_text):
            return jsonify({
                'error': 'Invalid encrypted text format'
            }), 400
        
        # Decrypt the message
        original_message, detected_emotion = cipher.decrypt(encrypted_text)
        
        logger.info(f"Decrypted message with emotion: {detected_emotion}")
        
        return jsonify({
            'original_message': original_message,
            'detected_emotion': detected_emotion,
            'emotion_key': cipher.get_emotion_key(detected_emotion)
        })
        
    except ValueError as e:
        return jsonify({
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Decryption error: {e}")
        return jsonify({
            'error': 'An unexpected error occurred during decryption'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'emotion_detector': emotion_detector is not None,
        'cipher': cipher is not None
    }
    
    if emotion_detector:
        try:
            # Test emotion detection
            test_emotion = emotion_detector.detect_emotion("Hello world")
            status['emotion_detector_test'] = test_emotion
        except Exception as e:
            status['emotion_detector_test'] = f'Error: {e}'
    
    return jsonify(status)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting Emotion Cipher application...")
    print("Server will be available at: http://localhost:5000")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
