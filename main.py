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
        text = recognizer.recognize_google(audio, language= 'es-ES')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Eres un asistente de tonalá chiapas"},
                    {"role": "user", "content": text},
            ]
        )

        print(f'Dijiste: {text}')

        result = ''
        for choices in response.choices:
            result += choices.message.content
        
        print(f'El bot dijo: {result}')
    except Exception as e:
        print(f'Error: {e}')