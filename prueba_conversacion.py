import openai
import os
from dotenv import load_dotenv

# Configura tu API key de OpenAI
load_dotenv()        
openai.api_key = os.getenv('API_KEY')

def obtener_respuesta(mensaje):
   respuesta = openai.Completion.create(
       engine="text-davinci-002",
       prompt=f"Bot: {mensaje}\nUsuario:",
       temperature=0.7,
   )
   return respuesta.choices[0].text.strip()

# Inicia la conversación
conversacion = []

while True:
   entrada_usuario = input("Usuario: ")
   conversacion.append(f"Usuario: {entrada_usuario}")

   respuesta_bot = obtener_respuesta("\n".join(conversacion))
   conversacion.append(f"Bot: {respuesta_bot}")
   print(f"Bot: {respuesta_bot}")