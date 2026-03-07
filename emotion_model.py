from transformers import pipeline
import torch
import re

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detection model"""
        try:
            # Use a smaller, faster model for quick startup
            self.classifier = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-roberta-base-emotion",
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1
            )
            print("Emotion model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using keyword-based emotion detection as fallback")
            self.classifier = None
    
    def detect_emotion_with_confidence(self, text):
        """
        Detect emotion from text with confidence score
        
        Args:
            text (str): Input text
            
        Returns:
            tuple: (emotion, confidence_score)
        """
        if not text or not text.strip():
            return "neutral", 0.5
        
        # Try AI model first if available
        if self.classifier:
            try:
                results = self.classifier(text)[0]
                best_result = max(results, key=lambda x: x['score'])
                emotion = best_result['label'].lower()
                confidence = best_result['score']
                
                # Map to our standard emotions
                emotion_mapping = {
                    'joy': 'joy', 'happiness': 'joy', 'happy': 'joy', 'love': 'joy',
                    'sadness': 'sadness', 'sad': 'sadness', 'disappointment': 'sadness',
                    'anger': 'anger', 'angry': 'anger', 'annoyance': 'anger', 'fury': 'anger',
                    'fear': 'fear', 'scared': 'fear', 'anxiety': 'fear', 'nervous': 'fear',
                    'surprise': 'surprise', 'surprised': 'surprise', 'shock': 'surprise',
                    'enthusiasm': 'joy', 'excitement': 'joy', 'pride': 'joy',
                    'disgust': 'anger', 'contempt': 'anger',
                    'neutral': 'neutral', 'calm': 'neutral', 'relaxed': 'neutral'
                }
                
                mapped_emotion = emotion_mapping.get(emotion, self._infer_emotion_from_keywords(text))
                return mapped_emotion, confidence
                
            except Exception as e:
                print(f"AI model error: {e}")
        
        # Fallback to keyword detection
        emotion = self._infer_emotion_from_keywords(text)
        return emotion, 0.8 if emotion != 'neutral' else 0.6
    
    def _infer_emotion_from_keywords(self, text):
        """Keyword-based emotion detection"""
        text_lower = text.lower()
        
        # Joy keywords
        joy_patterns = [
            r'\b(happy|joy|excited|wonderful|amazing|great|love|fantastic|awesome|brilliant|excellent|perfect|glad|delighted|thrilled|ecstatic)\b',
            r'\b(smile|laugh|celebrate|cheer|enjoy|pleased|satisfied|content)\b'
        ]
        
        # Sadness keywords
        sadness_patterns = [
            r'\b(sad|cry|depressed|unhappy|miserable|terrible|awful|disappointed|hurt|grief|sorrow|lonely|heartbroken|devastated)\b',
            r'\b(tear|weep|mourn|regret|miss|longing|empty)\b'
        ]
        
        # Anger keywords
        anger_patterns = [
            r'\b(angry|mad|furious|annoyed|frustrated|hate|disgusted|irritated|rage|outraged|infuriated|resentful)\b',
            r'\b(damn|stupid|ridiculous|unbelievable|outrageous|insane)\b'
        ]
        
        # Fear keywords
        fear_patterns = [
            r'\b(scared|afraid|terrified|fear|worried|anxious|nervous|panic|phobia|dread|horrified)\b',
            r'\b(threat|danger|risk|scary|frightening|alarming|concerned)\b'
        ]
        
        # Surprise keywords
        surprise_patterns = [
            r'\b(surprised|shocked|amazed|astonished|unexpected|sudden|wow|whoa|incredible|unbelievable)\b',
            r'\b(astonished|stunned|bewildered|perplexed|confused)\b'
        ]
        
        # Check patterns in order of priority
        for pattern in joy_patterns:
            if re.search(pattern, text_lower):
                return 'joy'
        
        for pattern in sadness_patterns:
            if re.search(pattern, text_lower):
                return 'sadness'
        
        for pattern in anger_patterns:
            if re.search(pattern, text_lower):
                return 'anger'
        
        for pattern in fear_patterns:
            if re.search(pattern, text_lower):
                return 'fear'
        
        for pattern in surprise_patterns:
            if re.search(pattern, text_lower):
                return 'surprise'
        
        return 'neutral'
    
    def detect_emotion(self, text):
        """
        Detect emotion from text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Detected emotion (joy, sadness, anger, fear, surprise, or neutral)
        """
        emotion, _ = self.detect_emotion_with_confidence(text)
        return emotion
    
    def create_emotion_fingerprint(self, text):
        """
        Create emotion fingerprint with confidence
        
        Args:
            text (str): Input text
            
        Returns:
            str: Emotion fingerprint (e.g., "Joy-82")
        """
        emotion, confidence = self.detect_emotion_with_confidence(text)
        confidence_percent = int(confidence * 100)
        return f"{emotion.capitalize()}-{confidence_percent}"
    
    def get_emotion_confidence(self, text):
        """
        Get emotion detection confidence scores
        
        Args:
            text (str): Input text
            
        Returns:
            dict: Dictionary with emotions as keys and confidence scores as values
        """
        if not self.classifier:
            return {"neutral": 1.0}
        
        if not text or not text.strip():
            return {"neutral": 1.0}
        
        try:
            results = self.classifier(text)[0]
            confidence_dict = {}
            
            for result in results:
                emotion = result['label'].lower()
                confidence = result['score']
                confidence_dict[emotion] = confidence
            
            return confidence_dict
            
        except Exception as e:
            print(f"Error getting emotion confidence: {e}")
            return {"neutral": 1.0}
