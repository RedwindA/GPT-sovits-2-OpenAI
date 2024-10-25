from flask import Flask, request, send_file
import requests
from pydub import AudioSegment
import io
import os  # Import os to access environment variables

app = Flask(__name__)

# Get API_KEY from environment variable
API_KEY = os.environ.get('API_KEY')
# Get BACKEND_URL from environment variable or use default
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://127.0.0.1:9880')

# Get other parameters from environment variables or use default values
TEXT_LANGUAGE = os.environ.get('TEXT_LANGUAGE', 'zh')
TOP_K = int(os.environ.get('TOP_K', 15))
TOP_P = float(os.environ.get('TOP_P', 1))
TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.45))
SPEED = float(os.environ.get('SPEED', 0.95))

# Print all parameters in one line for debugging
print(f"BACKEND_URL: {BACKEND_URL}, TEXT_LANGUAGE: {TEXT_LANGUAGE}, TOP_K: {TOP_K}, TOP_P: {TOP_P}, TEMPERATURE: {TEMPERATURE}, SPEED: {SPEED}")

@app.route('/v1/audio/speech', methods=['POST'])
def convert_tts():
    # Check API key if it's set in environment
    if API_KEY:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return "Missing Authorization header", 401
        
        # Check if header starts with "Bearer "
        if not auth_header.startswith('Bearer '):
            return "Invalid Authorization header format", 401
        
        # Extract and verify API key
        provided_key = auth_header.split(' ')[1]
        if provided_key != API_KEY:
            return "Invalid API key", 401

    # Extract 'input' field from OpenAI request
    openai_data = request.json
    text = openai_data.get('input')

    # Construct backend request body
    backend_payload = {
        "text": text,
        "text_language": TEXT_LANGUAGE,
        "top_k": TOP_K,
        "top_p": TOP_P,
        "temperature": TEMPERATURE,
        "speed": SPEED
    }

    # Send request to backend
    backend_response = requests.post(BACKEND_URL, json=backend_payload)

    # Check if the backend response is successful
    if backend_response.status_code != 200:
        return f"Backend service error: {backend_response.text}", backend_response.status_code

    # Convert returned WAV file to MP3
    wav_audio = io.BytesIO(backend_response.content)
    audio = AudioSegment.from_wav(wav_audio)
    mp3_audio = io.BytesIO()
    audio.export(mp3_audio, format="mp3")
    mp3_audio.seek(0)

    # Return MP3 file
    return send_file(mp3_audio, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)