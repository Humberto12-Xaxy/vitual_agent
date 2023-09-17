import speech_recognition as sr
from ia import IA
from instructions import Instruction
import json
import os
from subprocess import call

recognizer = sr.Recognizer()

instruction = Instruction()

os.environ['PATH'] += os.pathsep + 'C:\PATH_Programs'

while True:
    with sr.Microphone() as source:

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
            function_response = {'intrucciones': instruction.get_content_file(), 'mas_ayuda' : 'Le voy a comunicar con una persona de soporte tecnico para que puedan agendar una cita'}
            function_response = json.dumps(function_response)
            
            final_response = ia.process_response(text, message, function_name, function_response)



            print(f'El bot dijo: {final_response}')

        except Exception as e:
            print(f'Error: {e}')