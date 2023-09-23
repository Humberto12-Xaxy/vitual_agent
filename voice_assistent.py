from contextlib import closing
import json
import os
import threading
import time

import speech_recognition as sr

from tempfile import gettempdir
import boto3
import pygame

from ia import IA
from instructions import Instruction

class VoiceAssistent:

    def __init__(self) -> None:  
        self.polly = boto3.client('polly', region_name= 'us-east-1', aws_access_key_id= 'AKIAZ3FMUPPGFUKTQRPG', aws_secret_access_key= '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')
        
        self.function_name = None
        self.args = None
        self.message = ''
        
        self.text = ''
        self.final_response = ''
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.ia = IA()
        self.instruction = Instruction()
        
        self.active = True
        self.is_speaking = False

        

    def listen_start(self):
        self.listen_thread = threading.Thread(target= self.listen)
        self.listen_thread.start()

    def listen(self):
        while self.text.lower() != 'detener':
            with self.microphone as source:
                print('Entre al with')
                try:
                    self.recognizer.adjust_for_ambient_noise(source)
                    print('Escuchando')
                    audio = self.recognizer.listen(source)
                    
                    self.text = self.recognizer.recognize_google(audio, language= 'es-MX')
                    print(f'Dijiste: {self.text}')

                    if self.text.lower() == 'detener' and self.is_speaking:
                        self.stop_audio()
                except Exception as e:
                    print(f'Error: {e}')
        
        else:
            self.active = False
            
    def synthesize_speech(self, text):

        response = self.polly.synthesize_speech(
                                    Engine="neural",
                                    Text = text, 
                                    LanguageCode="es-MX",
                                    OutputFormat="mp3",
                                    VoiceId="Andres")
    
        if 'AudioStream' in response:
            with closing(response["AudioStream"]) as stream:
                self.output = os.path.join(gettempdir(), 'speech.mp3')

                with open(self.output, 'wb') as file:
                    file.write(stream.read())
    

    def resquest_ia(self):
        
        if self.text != '':
            self.function_name, self.args, self.message = self.ia.process_funtions(self.text)
    

    def response_ia(self):
        print(f'function_name : {self.function_name}')
        
        if self.text != 'detener':
            if self.function_name == 'no_internet_service':
                
                # conversation = []
                # conversation.append({'role' : 'system', 'content' : 'Eres un agente telefónico de call center que trabaja para la empresa de IZZI, pregunta acerca de su problema o si requiere información'})
                
                # while True:
                #     conversation.append({"role": "user", "content": self.text})
                    
                #     self.final_response = self.ia.conversarion(conversation)

                #     self.synthesize_speech(self.final_response)
                #     self.play_audio()

                #     conversation.append({"role": "system", "content": self.final_response})

                function_response = {'intrucciones': self.instruction.no_internet_service()}
                function_response = json.dumps(function_response)

                start_time = time.time()
                self.final_response = self.ia.process_response(self.text, self.message, self.function_name, function_response)
                end_time = time.time()

                tiempo_transcurrido = end_time - start_time

                print(f'Tiempo de ejecucion de la funcion: {tiempo_transcurrido}')

                print('Respondiendo...')
                self.synthesize_speech(self.final_response)
                self.play_audio()
            
            else:
                function_response = {'ayudar en lo que necesite': 'Dar instrucciones de lo que el cliente pida correspondiendo a algun problema de IZZI'}
                function_response = json.dumps(function_response)

                self.final_response = self.ia.process_response(self.text, self.message, '', function_response)
                print('Respondiendo...')
                self.synthesize_speech(self.final_response)
                self.play_audio()


    def play_audio(self):
        
        self.is_speaking = True
        pygame.init()   
        sound = pygame.mixer.Sound(self.output)

        sound.play()

        while pygame.mixer.get_busy():
            pass

        pygame.quit()
        self.is_speaking = False

    def stop_audio(self):
        pygame.mixer.stop()
        self.is_speaking = False

if __name__ == '__main__':

    voice_assistent = VoiceAssistent()

    saludo = voice_assistent.ia.call_intro()

    voice_assistent.synthesize_speech(saludo)
    voice_assistent.play_audio()

    voice_assistent.listen_start()

    while voice_assistent.active:

        if voice_assistent.text != '':
            voice_assistent.resquest_ia()
            voice_assistent.response_ia()
            voice_assistent.text = ''
    
    voice_assistent.listen_thread.join()
        