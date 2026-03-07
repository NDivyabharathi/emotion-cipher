import json
import os
from datetime import datetime

class DataStorage:
    def __init__(self, data_file='data_store.json'):
        """Initialize data storage"""
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def _save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def store_encryption(self, encrypted_text, original_message, emotion, confidence):
        """
        Store encryption mapping
        
        Args:
            encrypted_text (str): Encrypted text
            original_message (str): Original message
            emotion (str): Detected emotion
            confidence (float): Confidence score
        """
        self.data[encrypted_text] = {
            'original_message': original_message,
            'emotion': emotion,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        self._save_data()
    
    def get_decryption_data(self, encrypted_text):
        """
        Get decryption data for encrypted text
        
        Args:
            encrypted_text (str): Encrypted text
            
        Returns:
            dict: Decryption data or None if not found
        """
        return self.data.get(encrypted_text)
    
    def is_encrypted_text_stored(self, encrypted_text):
        """Check if encrypted text exists in storage"""
        return encrypted_text in self.data
    
    def get_all_stored_data(self):
        """Get all stored data"""
        return self.data
    
    def clear_old_data(self, days_old=30):
        """Clear data older than specified days"""
        current_time = datetime.now()
        keys_to_remove = []
        
        for encrypted_text, data in self.data.items():
            try:
                timestamp = datetime.fromisoformat(data['timestamp'])
                if (current_time - timestamp).days > days_old:
                    keys_to_remove.append(encrypted_text)
            except:
                keys_to_remove.append(encrypted_text)
        
        for key in keys_to_remove:
            del self.data[key]
        
        if keys_to_remove:
            self._save_data()
        
        return len(keys_to_remove)
