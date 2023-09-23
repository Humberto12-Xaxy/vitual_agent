import openai
import os
from dotenv import load_dotenv

# Configura tu API key de OpenAI
load_dotenv()        
openai.api_key = os.getenv('API_KEY')

# Conversacion inicial
conversacion = []

while True:
    # Obtiene la entrada del usuario
    usuario_input = input("Tú: ")

    # Agrega la entrada del usuario a la conversación
    conversacion.append({"role": "user", "content": usuario_input})

    # Envía la conversación actual al modelo de OpenAI
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversacion
    )

    # Obtiene la respuesta del modelo
    respuesta_modelo = respuesta["choices"][0]["message"]["content"]

    # Imprime la respuesta del modelo
    print("Modelo:", respuesta_modelo)

    # Agrega la respuesta del modelo a la conversación
    conversacion.append({"role": "assistant", "content": respuesta_modelo})