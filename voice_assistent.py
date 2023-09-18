from contextlib import closing
import os
from tempfile import gettempdir
import boto3
import pygame

class VoiceAssistent:

    def __init__(self) -> None:  
        self.polly = boto3.client('polly', region_name= 'us-east-1', aws_access_key_id= 'AKIAZ3FMUPPGFUKTQRPG', aws_secret_access_key= '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')


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
    
    def play_audio(self):
        
        pygame.init()
        sound = pygame.mixer.Sound(self.output)

        sound.play()

        while pygame.mixer.get_busy():
            pass

        pygame.quit()

