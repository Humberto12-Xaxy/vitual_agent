from dotenv import load_dotenv
import os
import speech_recognition as sr
import openai
import threading
import queue

load_dotenv()

# Configura tu token de OpenAI
openai.api_key = os.getenv('API_KEY')

shared_queue = queue.Queue()

def listen_for_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)  # Ajusta para eliminar el ruido de fondo
        print("Escuchando... Di 'detener' para finalizar.")
        
        while True:
            try:
                audio = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio, language='es-MX')
                print(f"Usuario: {user_input}")
                shared_queue.put(user_input)
                if "detener" in user_input.lower():
                    print("Deteniendo...")
                    break
                
                # Continúa el procesamiento de la entrada del usuario aquí
            except Exception as e:
                print(e)

def openai_thread():
    while True:
        
        try:
            data = shared_queue.get()
            if "detener" in data.lower():
                print("Deteniendo...")
                break

            print("AI: Procesando respuesta...")
            response = openai.ChatCompletion.create(
                model = 'gpt-3.5-turbo-0613',
                messages = [
                    {'role': 'system', 'content': 'Eres un agente telefónIco de call center que trabaja para la empresa de IZZI'},
                    {'role': 'system', 'content': data}, 
                ], 
            )

            print("AI:", response['choices'][0]['message']['content'])
        except Exception as e:
            print(e)
if __name__ == "__main__":
    audio_thread = threading.Thread(target=listen_for_audio)
    ai_thread = threading.Thread(target=openai_thread)

    audio_thread.start()
    ai_thread.start()

    audio_thread.join()
    ai_thread.join()