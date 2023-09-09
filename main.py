import speech_recognition as sr
import openai
import os
from dotenv import load_dotenv

load_dotenv()

recognizer = sr.Recognizer()
openai.api_key = os.getenv('API_KEY')

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source)
    print('Escuchando...')
    audio = recognizer.listen(source)
    
    try:
        print('Reconociendo...')
        text = openai.Audio.transcribe(model= 'whisper-1',file= audio)
        print(f'Dijiste: {text["text"]}')
    
    except Exception as e:
        print(f'Error: {e}')