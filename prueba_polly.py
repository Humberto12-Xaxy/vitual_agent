from contextlib import closing
import os
from tempfile import gettempdir
import boto3 
from boto3 import Session
import pygame
import playsound
from pydub.playback import play

session = Session()

polly = boto3.client('polly', region_name= 'us-east-1', aws_access_key_id= 'AKIAZ3FMUPPGFUKTQRPG', aws_secret_access_key= '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')

text = 'hola, como estás me llamo Andrés aqlasdqoj asnasndoq  qwqow bdiqwb qwdkasbdkb asdasd qwd asd asdqw dasd q'

# Cambiar por Mia
response = polly.synthesize_speech(
                                    Engine="neural",
                                    Text = text, 
                                    LanguageCode="es-MX",
                                    OutputFormat="mp3",
                                    VoiceId="Andres")

if 'AudioStream' in response:

    with closing(response["AudioStream"]) as stream:
        output = os.path.join(gettempdir(), 'speech.mp3')

        with open(output, 'wb') as file:
            file.write(stream.read())

sound = playsound.playsound(output)


pygame.init()

sound = pygame.mixer.Sound(output)

sound.play()



# # Cerrar Pygame
pygame.quit()

