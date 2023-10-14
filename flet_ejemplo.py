import flet
from flet import (
    Page,
    Image
)

from voice_assistent import VoiceAssistent

def main(page: Page):
    
    voice_assistent = VoiceAssistent()

    page.title = "Bot"
    page.horizontal_alignment = "center"
    page.vertical_alignment = 'center'
    page.update()

    saludo = voice_assistent.ia.call_intro()

    voice_assistent.listen_start()
    voice_assistent.speak_when_silence_start()

    image = Image(src= './image/bot_speaking.gif', width= 300, height= 300)
    # add application's root control to the page
    
    page.add(
        image
    )

    voice_assistent.synthesize_speech(saludo)
    voice_assistent.play_audio()

    while voice_assistent.active:
        if voice_assistent.text != '':

            response = voice_assistent.response_ia()
            
            if not voice_assistent.is_speaking:
                voice_assistent.response = ''
                image.src = './image/bot_speaking.gif'
                page.update()
                voice_assistent.synthesize_speech(response)
                voice_assistent.play_audio()

            
            image.src = './image/bot_escucha.gif'
            page.update()
            
            voice_assistent.text = ''

        else:
            image.src = './image/bot_escucha.gif'
            page.update()


    voice_assistent.listen_thread.join()
    voice_assistent.speak_when_silence_thread.join()

flet.app(target=main)