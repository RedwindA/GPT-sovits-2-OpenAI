from flask import Flask, request, send_file, jsonify
import requests
from pydub import AudioSegment
import io
import os  # Import os to access environment variables
import json
import yaml

app = Flask(__name__)

# Get API_KEY from environment variable
API_KEY = os.environ.get('API_KEY')

# Get BACKEND_URL from environment variable or use default
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://127.0.0.1:9880')

# Load YAML configuration file
def load_voice_config():
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            voices = config.get('voices', {})
            
            voice_mapping = {
                voice: voice_data['models']
                for voice, voice_data in voices.items()
            }
            refer_mapping = {
                voice: voice_data['refer']
                for voice, voice_data in voices.items()
            }
            return voice_mapping, refer_mapping
    except Exception as e:
        print(f"Error loading config.yaml: {e}")
        return {}, {}

# Replace original environment variable configuration
VOICE_MAPPING, REFER_MAPPING = load_voice_config()

# Get other parameters from environment variables or use default values
TEXT_LANGUAGE = os.environ.get('TEXT_LANGUAGE', 'zh')
TOP_K = int(os.environ.get('TOP_K', 15))
TOP_P = float(os.environ.get('TOP_P', 1))
TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.45))
SPEED = float(os.environ.get('SPEED', 0.95))

# Print all parameters in one line for debugging
print(f"BACKEND_URL: {BACKEND_URL}, TEXT_LANGUAGE: {TEXT_LANGUAGE}, TOP_K: {TOP_K}, TOP_P: {TOP_P}, TEMPERATURE: {TEMPERATURE}, SPEED: {SPEED}, VOICE_MAPPING: {VOICE_MAPPING}")

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
    voice = openai_data.get('voice')

    # Get model paths and refer from the VOICE_MAPPING according to the provided voice
    voice_config = VOICE_MAPPING.get(voice)
    refer_config = REFER_MAPPING.get(voice)

    if not voice_config:
        return f"Voice '{voice}' is not supported", 400

    gpt_model_path = voice_config.get('gpt_model_path')
    sovits_model_path = voice_config.get('sovits_model_path')
    refer_wav_path = refer_config.get('refer_wav_path')
    prompt_text = refer_config.get('prompt_text')

    if not gpt_model_path or not sovits_model_path:
        return f"Model paths for voice '{voice}' are missing", 500

    if not refer_wav_path or not prompt_text:
        return f"Refer for voice '{voice}' are missing", 500
    
    # Step 1: Set the models in the backend
    set_model_response = requests.post(f"{BACKEND_URL}/set_model", json={
        "gpt_model_path": gpt_model_path,
        "sovits_model_path": sovits_model_path
    })


    # Check if the backend was able to set the models and refer
    if set_model_response.status_code != 200:
        return f"Backend failed to set models: {set_model_response.text}", set_model_response.status_code
     

    # Step 2: Send text-to-speech request to the backend
    backend_payload = {
        "text": text,
        "text_language": TEXT_LANGUAGE,
        "refer_wav_path": refer_wav_path,
        "prompt_text": prompt_text,
        "prompt_language": TEXT_LANGUAGE, # Add language for prompt text to pass validation
        "top_k": TOP_K,
        "top_p": TOP_P,
        "temperature": TEMPERATURE,
        "speed": SPEED
    }

    backend_response = requests.post(BACKEND_URL, json=backend_payload)

    # Check if the backend response is successful
    if backend_response.status_code != 200:
        return f"Backend service error: {backend_response.text}", backend_response.status_code

    # Step 3: Convert returned WAV file to MP3
    wav_audio = io.BytesIO(backend_response.content)
    audio = AudioSegment.from_wav(wav_audio)
    mp3_audio = io.BytesIO()
    audio.export(mp3_audio, format="mp3")
    mp3_audio.seek(0)

    # Return MP3 file
    return send_file(mp3_audio, mimetype='audio/mp3', as_attachment=True, download_name='speech.mp3')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)