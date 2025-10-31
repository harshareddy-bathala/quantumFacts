# Kyutai TTS Setup on Google Colab

This guide will help you set up Kyutai TTS on Google Colab to use free GPU for high-quality text-to-speech generation.

## Prerequisites

- Google Account
- Basic understanding of Python

## Setup Steps

### 1. Create a New Colab Notebook

1. Go to [Google Colab](https://colab.research.google.com/)
2. Click "New Notebook"
3. Name it "Kyutai TTS Server"

### 2. Install Kyutai TTS

In the first cell, run:

```python
!pip install moshi
```

### 3. Set Up TTS Server

Create a new cell with this code:

```python
import torch
from moshi import MoshiTTS
from flask import Flask, request, jsonify
import base64
import json

# Initialize TTS model
print("Loading Kyutai TTS model...")
tts = MoshiTTS()
print("Model loaded successfully!")

# Create Flask app
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_speech():
    try:
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', 'default')
        speed = data.get('speed', 1.0)
        
        # Generate speech
        audio, word_timestamps = tts.synthesize(
            text,
            voice=voice,
            speed=speed,
            return_word_timestamps=True
        )
        
        # Encode audio to base64
        audio_base64 = base64.b64encode(audio.numpy().tobytes()).decode('utf-8')
        
        response = {
            'audio_base64': audio_base64,
            'word_timestamps': word_timestamps,
            'sample_rate': 24000
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### 4. Expose with ngrok

In a new cell:

```python
!pip install pyngrok

from pyngrok import ngrok

# Set your ngrok auth token (get free one from ngrok.com)
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Create tunnel
public_url = ngrok.connect(5000)
print(f"TTS Server URL: {public_url}")
```

### 5. Get Your Server URL

After running the above cells, you'll get a URL like:
```
https://xxxx-xx-xxx-xxx-xxx.ngrok.io
```

Copy this URL and add it to your `.env` file:
```bash
COLAB_NOTEBOOK_URL=https://xxxx-xx-xxx-xxx-xxx.ngrok.io
```

## Usage in Main Application

The main application will automatically use this Colab server for TTS generation:

```python
from viral_shorts.narration.tts import KyutaiTTS

tts = KyutaiTTS()
result = tts.generate_speech("Hello world!")
```

## Important Notes

1. **Session Duration**: Free Colab sessions last ~12 hours
2. **GPU Access**: You get limited free GPU time per day
3. **Reconnection**: You'll need to restart the notebook and get a new URL periodically
4. **Alternative**: For production, consider:
   - Colab Pro for longer sessions
   - Self-hosted GPU server
   - Alternative TTS services (Coqui TTS, XTTS, etc.)

## Troubleshooting

**Connection timeout:**
- Check if Colab session is still running
- Verify ngrok tunnel is active
- Update COLAB_NOTEBOOK_URL in .env

**Out of memory:**
- Restart runtime
- Use Colab Pro for more RAM

**API errors:**
- Check ngrok auth token
- Verify Flask app is running
- Test /health endpoint

## Alternative TTS Options

If Colab setup is too complex, consider:

1. **Local CPU TTS** (slower but works):
   - Coqui TTS
   - pyttsx3
   - gTTS (Google TTS)

2. **Cloud TTS** (may have costs):
   - Google Cloud TTS (free tier available)
   - Amazon Polly
   - Microsoft Azure TTS

3. **Open Source**:
   - Mozilla TTS
   - Piper TTS
   - FastSpeech2

## Free GPU Alternatives

- **Kaggle Notebooks**: Similar to Colab, 30 hours/week GPU
- **Paperspace Gradient**: Free tier available
- **Lightning.ai**: Free GPU hours

---

**Note**: The actual Kyutai TTS API might differ. This is a template showing the expected integration pattern. Check Kyutai documentation for exact implementation.
