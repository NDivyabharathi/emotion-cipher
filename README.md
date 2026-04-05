# Emotion Cipher – Emotion Aware Encryption

A web application that encrypts text messages while detecting their emotional tone using AI, and allows decryption back to the original message.

## Features

- **AI-Powered Emotion Detection**: Uses HuggingFace transformers to detect emotions (joy, sadness, anger, fear, surprise, neutral)
- **Emotion-Based Encryption**: Each emotion maps to a unique encryption key
- **Secure Encryption**: Base64 encoding with emotion-specific keys
- **Easy Decryption**: Decrypt messages back to their original form
- **Modern UI**: Professional Bootstrap-based interface with responsive design
- **Real-time Processing**: Fast encryption and decryption with visual feedback

## Tech Stack

- **Backend**: Python Flask
- **AI Model**: HuggingFace transformers (emotion classification)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Encryption**: Custom Emotion Cipher algorithm with Base64 encoding

## Installation

1. Navigate to the project directory:
```bash
cd emotion-cipher
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## Project Structure

```
emotion-cipher/
├── app.py                 # Main Flask application with API endpoints
├── emotion_model.py       # Emotion detection using HuggingFace transformers
├── cipher.py             # Emotion Cipher encryption/decryption logic
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/
│   └── index.html       # Main HTML template with Bootstrap UI
└── static/
    ├── style.css        # Custom CSS styling
    └── script.js        # JavaScript frontend functionality
```

## API Endpoints

### POST /encrypt
Encrypt a message with emotion detection.

**Request:**
```json
{
    "message": "Your message here"
}
```

**Response:**
```json
{
    "encrypted_text": "base64_encoded_encrypted_message",
    "detected_emotion": "joy",
    "emotion_key": "JY9"
}
```

### POST /decrypt
Decrypt an encrypted message.

**Request:**
```json
{
    "encrypted_text": "base64_encoded_encrypted_message"
}
```

**Response:**
```json
{
    "original_message": "Your original message",
    "detected_emotion": "joy",
    "emotion_key": "JY9"
}
```

### GET /health
Health check endpoint to verify server status.

## Emotion Mapping

Each emotion is mapped to a unique encryption key:

- **joy** → JY9
- **sadness** → SD3
- **anger** → AN7
- **fear** → FR2
- **surprise** → SP8
- **neutral** → NT5

## Encryption Process

1. User enters a text message
2. AI detects the emotional tone of the message
3. Emotion is mapped to a specific key
4. Message + emotion key are combined
5. Result is encoded using Base64
6. Encrypted text is displayed

## Decryption Process

1. Encrypted text is Base64 decoded
2. Emotion key is extracted
3. Original message is recovered
4. Detected emotion is displayed

## Usage

1. **Encrypt a Message**:
   - Type your message in the input box
   - Click "Encrypt Message"
   - View the encrypted text and detected emotion

2. **Decrypt a Message**:
   - Ensure encrypted text is in the encrypted field
   - Click "Decrypt Message"
   - View the original message and detected emotion

3. **Copy Encrypted Text**:
   - Click the clipboard icon to copy encrypted text to clipboard

## Browser Compatibility

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

## Dependencies

- **flask**: Web framework
- **transformers**: HuggingFace AI models
- **torch**: PyTorch for AI model processing
- **numpy**: Numerical computations
- **requests**: HTTP library (for potential API calls)

## Security Notes

- Messages are encrypted using Base64 encoding with emotion-specific keys
- The system is designed for demonstration and educational purposes
- For production use, consider additional security measures

## Troubleshooting

### Common Issues

1. **Model Loading Errors**:
   - Ensure all dependencies are installed correctly
   - Check internet connection for downloading AI models

2. **Port Already in Use**:
   - Change the port in `app.py` or stop other services using port 5000

3. **CORS Issues**:
   - The application runs on localhost, so CORS should not be an issue

### Performance Tips

- First AI model load may take a few seconds
- Subsequent requests will be faster
- Consider GPU acceleration if available

## License

This project is for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests!

