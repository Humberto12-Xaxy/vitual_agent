from contextlib import closing
import io
from tempfile import gettempdir
from elevenlabs import voices, generate, play, set_api_key, Voice, VoiceSettings
from dotenv import load_dotenv
import os
import elevenlabs
import pygame

pygame.init()

load_dotenv()
# 3qgBRQoNma81GU0oOMdB
set_api_key(os.getenv('ELEVENLABS_API_KEY'))

audio = generate(
    text = 'Que onda veguetta, vamos por las cariñosas',
    model= 'eleven_multilingual_v2',
    voice= Voice(
        voice_id= '3qgBRQoNma81GU0oOMdB',
        settings= VoiceSettings(stability=.7, similarity_boost=0.2, style=0.01, use_speaker_boost=False)
    ),
    stream= True
)

with closing(audio) as stream:
    output = os.path.join(gettempdir(), 'speech.mp3')
    print(stream)

    # Convert the generator object to a byte stream
    byte_stream = io.BytesIO()

    # Wrap the generator object in another generator object that reads the data in chunks
    # and writes it to the byte stream.
    for chunk in stream:
        byte_stream.write(chunk)

    with open(output, 'wb') as file:
        # Write the byte stream to the file
        file.write(byte_stream.getvalue())

sound = pygame.mixer.Sound(output)

sound.play()

while pygame.mixer.get_busy():
    pass
# play(audio)

# elevenlabs.stop()