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

# print(voices())
audio = generate(
    text = 'Que onda veguetta, vamos por las cariñosas',
    model= 'eleven_multilingual_v2',
    voice= Voice(
        voice_id= 'Ou8RTQTpWI3OiSkrgKeE',
        # settings= VoiceSettings(stability=.7, similarity_boost=0.2, style=0.01, use_speaker_boost=False)
    ),
    stream= True
)

# Convert the generator object to a byte stream
byte_stream = io.BytesIO()

# Wrap the generator object in another generator object that reads the data in chunks
# and writes it to the byte stream.
for chunk in audio:
    byte_stream.write(chunk)

# Write the byte stream to a file
with open(os.path.join(gettempdir(), 'speech.mp3'), 'wb') as file:
    file.write(byte_stream.getvalue())

# Play the audio
sound = pygame.mixer.Sound(os.path.join(gettempdir(), 'speech.mp3'))
sound.play()

while pygame.mixer.get_busy():
    pass

# play(audio)

# elevenlabs.stop()