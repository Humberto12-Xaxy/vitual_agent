from contextlib import closing
import io
import json
import os
import threading
import time
from elevenlabs import generate, set_api_key, Voice, VoiceSettings

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
        
        self.text = ''
        self.response = ''
        self.elapsed_time = 0

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.ia = IA()
        
        self.active = True
        self.is_speaking = False

    def speak_when_silence_start(self):
        self.speak_when_silence_thread = threading.Thread(target= self.speak_when_silence)
        self.speak_when_silence_thread.start()

    def speak_when_silence(self):
        
        while self.active:
            if self.response == '' and self.elapsed_time > 5:
                
                self.is_speaking = True
                self.synthesize_speech('Estoy haciendo la busqueda de la información que requieres')
                self.play_audio()



    def listen_start(self):
        self.listen_thread = threading.Thread(target= self.listen)
        self.listen_thread.start()

    def listen(self):
        phrases = [
                'espera', 'espera un momento', 'disculpa', 
                'disculpa la interrupcion', 'permiteme un momento', 
                'dame un momento', 'permitame un momento', 'no me interesa', 
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
                        self.is_speaking = False

                    if self.text == 'reanuda' and not self.is_speaking:
                        self.resume_audio()
                        self.is_speaking = True
                        
                    
                    if self.text == 'reanuda' and not self.is_speaking:
                        self.resume_audio()
                    

                except sr.UnknownValueError:
                    print('No se pudo entender el audio')
                except sr.RequestError as e:
                    print(f'Error en la solicitud: {e}')
        
        self.active = False
            
    def synthesize_speech(self, text):
        # set_api_key(os.getenv('ELEVENLABS_API_KEY'))

        # audio = generate(
        #     text = text,
        #     model= 'eleven_multilingual_v2',
        #     voice= Voice(
        #         voice_id= 'Ou8RTQTpWI3OiSkrgKeE',
        #         # settings= VoiceSettings(stability=.7, similarity_boost=0.2, style=0.01, use_speaker_boost=False)
        #     ),
        #     stream= True,
        # )

        # with closing(audio) as stream:
        #     self.output = os.path.join(gettempdir(), 'speech.mp3')

        #     # Convert the generator object to a byte stream
        #     byte_stream = io.BytesIO()

        #     # Wrap the generator object in another generator object that reads the data in chunks
        #     # and writes it to the byte stream.
        #     for chunk in stream:
        #         byte_stream.write(chunk)

        #     with open(self.output, 'wb') as file:
        #         # Write the byte stream to the file
        #         file.write(byte_stream.getvalue())

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

    def response_ia(self):

        start_time = time.time()
        self.response = self.ia.conversation(self.text)
        end_time = time.time()

        self.elapsed_time = end_time - start_time
        if self.is_speaking:
            time.sleep(7)
            return self.response
        else:
            return self.response

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
        pygame.mixer.pause()
    
    def resume_audio(self):
        self.is_speaking = True
        pygame.mixer.unpause()

if __name__ == '__main__':

    voice_assistent = VoiceAssistent()

    saludo = voice_assistent.ia.call_intro()

    voice_assistent.listen_start()

    voice_assistent.synthesize_speech(saludo)
    voice_assistent.play_audio()


    while voice_assistent.active:

        if voice_assistent.text != '':

            voice_assistent.response_ia()
            voice_assistent.text = ''
    
    voice_assistent.listen_thread.join()
        