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

import os
from dotenv import load_dotenv

class VoiceAssistent:

    def __init__(self) -> None:  
        load_dotenv()
        self.polly = boto3.client('polly', region_name= 'us-east-1', aws_access_key_id = os.getenv('AWS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))
        
        self.function_name = None
        self.args = None
        self.message = ''
        
        self.text = ''
        self.final_response = ''
        
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.ia = IA()
        
        self.active = True
        self.is_speaking = False

        

    def listen_start(self):
        self.listen_thread = threading.Thread(target= self.listen)
        self.listen_thread.start()

    def listen(self):
        phrases = ['espera', 'espera un momento', 'disculpa', 
                   'disculpa la interrupcion', 'permiteme un momento', 
                   'dame un momento', 'permitame un momento', 
                ]
        while self.active:
            with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source)

            with self.microphone as source:
                try:
                    print('Escuchando')
                    audio = self.recognizer.listen(source)
                    
                    self.text = self.recognizer.recognize_google(audio, language= 'es-MX')
                    print(f'Dijiste: {self.text}')

                    if self.text in phrases and self.is_speaking:
                        self.stop_audio()
                except sr.UnknownValueError:
                    print('No se pudo entender el audio')
                except sr.RequestError as e:
                    print(f'Error en la solicitud: {e}')
        
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
            try:
                self.function_name, self.args, self.message = self.ia.process_funtions(self.text)
            except Exception as e:
                print(e)

    def response_ia(self):

        response = self.ia.conversation(self.text)

        return response

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
        self.is_speaking = False
        pygame.mixer.stop()
        

if __name__ == '__main__':

    voice_assistent = VoiceAssistent()

    saludo = voice_assistent.ia.call_intro()

    voice_assistent.listen_start()

    voice_assistent.synthesize_speech(saludo)
    voice_assistent.play_audio()


    while voice_assistent.active:

        if voice_assistent.text != '':
            # voice_assistent.resquest_ia()
            # voice_assistent.response_ia()
            voice_assistent.response_ia()
            voice_assistent.text = ''
    
    voice_assistent.listen_thread.join()
        