import asyncio
import json
import speech_recognition as sr
import openai
import pyttsx3

# Configura tu clave de API de OpenAI
openai.api_key = "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"

# Inicializa el motor de texto a voz
engine = pyttsx3.init()

# Variable para controlar la interrupción
interrupted = False

contexto = {"Cuenta": 12345678 , 
            "complementos activos": 'xvideos $80 pesos , netflix:$50 , pornub $200,calientes3000 $500', 
            "titular":'Erik Garcia' , 
            "Saldo": '$100'}

contexto = json.dumps(contexto)

# Función para reproducir la respuesta de la IA en voz
def speak_response(response):
    global interrupted
    engine.say(response)
    engine.runAndWait()
    interrupted = True

# Función para interactuar con la IA de forma asincrónica
async def interact_with_ai():
    
    global interrupted
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        print("Escuchando...")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"Usuario: {text}")

            # Verificar si el usuario quiere interrumpir
            if "Otras opciones" in text.lower() or 'No me interesa' in text.lower() or 'Otra solucion' in text.lower():
                print("Usuario: Interrumpir")
                interrupted = True

            else:
                # Envía la pregunta del usuario a GPT-3 para obtener una respuesta
                completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Actua como un agente telefonico de call center de izzi,valida la cuenta y nombre antes dar un respuesta,el cliente tiene que dar los datos requeridos (cuenta y nombre del titular), analiza la matriz:{contexto} y brindame una solucion si hay datos nesesarios ,  , solo dame informacion si tiene que ver con un problema de izzi , si pregunta cosas como dame un chiste pide que sea serio , si te doy un numero de cuenta buscalo en la matriz"},
                    {"role": "user", "content": text }
                    ]
                )
                # Obtén la respuesta de GPT-3
                ai_response = completion.choices[0].message["content"]
                print(f"IA: {ai_response}")

                # Reproduce la respuesta en voz
                respuesta = speak_response(ai_response)
                print(respuesta)
                

        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error al realizar la solicitud de reconocimiento de voz: {e}")

        await asyncio.sleep(1)  # Espera 1 segundo antes de volver a escuchar

if __name__ == "_main_":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(interact_with_ai())