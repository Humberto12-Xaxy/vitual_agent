import speech_recognition as sr
import openai
from ia import IA
from voice import Voice
import json
import os
from subprocess import call

recognizer = sr.Recognizer()
voice = Voice()

os.environ['PATH'] += os.pathsep + 'C:\PATH_Programs'

with sr.Microphone() as source:

    # audio = voice.generate_audio('Buenos días, habla al servicio de soporte de internet, ¿En que puedo ayudarle?')
    # voice.play(audio)

    recognizer.adjust_for_ambient_noise(source)
    print('Escuchando...')
    audio = recognizer.listen(source)

    try:
        print('Reconociendo...')
        text = recognizer.recognize_google(audio, language='es-MX')
        print(f'Dijiste: {text}')

        ia = IA()
        
        function_name, args, message = ia.process_funtions(text)
        
        # print(f'nombre de la funcion: {function_name} args: {args} menssage: {message}')
        function_response = {'saludo': 'Hola que tal'}
        function_response = json.dumps(function_response)
        
        final_response = ia.process_response(text, message, function_name, function_response)


        # audio = voice.generate_audio(final_response)
        # voice.play(audio)

        print(f'El bot dijo: {final_response}')

    except Exception as e:
        print(f'Error: {e}')