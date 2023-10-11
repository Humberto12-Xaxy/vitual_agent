import requests
import pygame

pygame.init()
url = "https://app.coqui.ai/api/v2/samples/xtts/stream"

payload = {
    "speed": 1,
    "language": "es",
    "voice_id": "714c825b-0009-4819-aad5-02adbdb42e69",
    "text": "Hola, como estás"
}
headers = {
    "accept": "audio/wav",
    "content-type": "application/json",
    "authorization": "Bearer tgPuyY8f5k9hmiUFPoPcqjcdQ7fBUk2ELmKOY8aF3A6mW5g3lYZv0jtxZpyB33PA"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 201:

    pygame.event.get()

    # audio = bytes(response.content)

    sound = pygame.mixer.Sound('./output.wav')
    
    sound.play()

    while pygame.mixer.get_busy():
        pass
    
    pygame.quit()
    # Abre un archivo en modo binario para escribir los datos de audio
    # with open("output.wav", "wb") as audio_file:
    #     audio_file.write(response.content)
    # print("Archivo de audio descargado exitosamente como 'output.wav'")
else:
    print("Error en la solicitud. Código de respuesta:", response.status_code)

