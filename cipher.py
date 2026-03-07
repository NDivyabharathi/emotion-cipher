import base64
import json

class EmotionCipher:
    def __init__(self):
        """Initialize the Emotion Cipher with emotion-to-key mappings"""
        self.emotion_keys = {
            'joy': 'JY9',
            'sadness': 'SD3',
            'anger': 'AN7',
            'fear': 'FR2',
            'surprise': 'SP8',
            'neutral': 'NT5'
        }
        
        # Reverse mapping for decryption
        self.key_to_emotion = {v: k for k, v in self.emotion_keys.items()}
    
    def encrypt(self, message, emotion):
        """
        Encrypt a message using the Emotion Cipher algorithm
        
        Args:
            message (str): Original message to encrypt
            emotion (str): Detected emotion
            
        Returns:
            str: Encrypted message
        """
        if not message:
            raise ValueError("Message cannot be empty")
        
        if emotion not in self.emotion_keys:
            emotion = 'neutral'
        
        # Get the emotion key
        emotion_key = self.emotion_keys[emotion]
        
        # Combine message with emotion key
        combined_data = {
            'message': message,
            'emotion_key': emotion_key
        }
        
        # Convert to JSON string
        json_data = json.dumps(combined_data)
        
        # Encode using Base64
        encrypted_bytes = base64.b64encode(json_data.encode('utf-8'))
        encrypted_text = encrypted_bytes.decode('utf-8')
        
        return encrypted_text
    
    def decrypt(self, encrypted_text):
        """
        Decrypt an encrypted message
        
        Args:
            encrypted_text (str): Encrypted message
            
        Returns:
            tuple: (original_message, detected_emotion)
        """
        if not encrypted_text:
            raise ValueError("Encrypted text cannot be empty")
        
        try:
            # Decode from Base64
            encrypted_bytes = encrypted_text.encode('utf-8')
            json_data = base64.b64decode(encrypted_bytes).decode('utf-8')
            
            # Parse JSON
            combined_data = json.loads(json_data)
            
            # Extract message and emotion key
            original_message = combined_data['message']
            emotion_key = combined_data['emotion_key']
            
            # Convert emotion key back to emotion
            detected_emotion = self.key_to_emotion.get(emotion_key, 'neutral')
            
            return original_message, detected_emotion
            
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def get_emotion_key(self, emotion):
        """
        Get the encryption key for a given emotion
        
        Args:
            emotion (str): Emotion name
            
        Returns:
            str: Corresponding emotion key
        """
        return self.emotion_keys.get(emotion.lower(), self.emotion_keys['neutral'])
    
    def validate_encrypted_format(self, encrypted_text):
        """
        Validate if the encrypted text has the correct format
        
        Args:
            encrypted_text (str): Encrypted text to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Try to decode and parse
            encrypted_bytes = encrypted_text.encode('utf-8')
            json_data = base64.b64decode(encrypted_bytes).decode('utf-8')
            combined_data = json.loads(json_data)
            
            # Check required fields
            return 'message' in combined_data and 'emotion_key' in combined_data
            
        except Exception:
            return False
