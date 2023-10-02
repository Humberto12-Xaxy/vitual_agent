import time
import speech_recognition as sr
from ia import IA
from instructions import Instruction
import json
import os
from subprocess import call
from voice_assistent import VoiceAssistent

recognizer = sr.Recognizer()

instruction = Instruction()

voice_polly = VoiceAssistent()

ia = IA()

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

            
            print('Analizando...')
            start_time = time.time()
            function_name, args, message = ia.process_funtions(text)
            end_time = time.time()
            tiempo_transcurrido = end_time - start_time
            print(f'Tiempo de ejecucion de la funcion: {tiempo_transcurrido}')

            if function_name is not None:
                if function_name == 'no_internet_service':
                    instruction.set_file('instrucciones.txt')
                    
                    function_response = {'intrucciones': instruction.get_content_file(), 'mas_ayuda' : 'Le voy a comunicar con una persona de soporte tecnico para que puedan agendar una cita'}
                    function_response = json.dumps(function_response)
                    
                    print('Respondiendo...')
                    final_response = ia.process_response(text, message, function_name, function_response)
                    
                    voice_polly.synthesize_speech(final_response)
                    voice_polly.play_audio()

                    print(f'El bot dijo: {final_response}')
                
                else:
                    function_response = {'mas_ayuda' : 'Le voy a comunicar con una persona de soporte tecnico para que puedan agendar una cita'}
                    function_response = json.dumps(function_response)
                    
                    print('Respondiendo...')
                    final_response = ia.process_response(text, message, function_name, function_response)

                    voice_polly.synthesize_speech(final_response)
                    voice_polly.play_audio()

                    print(f'El bot dijo: {final_response}')

            else: 
                function_response = 'Esta funcion no está programada en el sistema'

                print('Respondiendo...')
                voice_polly.synthesize_speech(function_response)
                voice_polly.play_audio()

                print(f'El bot dijo: {function_name}')

        except Exception as e:
            print(f'Error: {e}')