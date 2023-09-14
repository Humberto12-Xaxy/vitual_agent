from elevenlabs import generate, play
from dotenv import load_dotenv
import os

class Voice:

    def __init__(self) -> None:
        load_dotenv()
        os.getenv('ELEVENLABS_API_KEY')
    
    def generate_audio(self, text):

        audio = generate(
            text= text,
            voice= 'Charlotte',
            model= 'eleven_multilingual_v2'
        )

        return audio

    def play(self, audio):
        play(audio)