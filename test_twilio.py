from twilio.rest import Client
from fastapi import FastAPI

from twilio.twiml.voice_response import VoiceResponse
app = FastAPI()

# account_sid = 'AC7e5eb2eb42ace45c24794cc2ee0a41e2'
# auth_token = '5f66892904be381f4f271c97a45ffd7a'

# client = Client(account_sid, auth_token)

# call = client.calls.create(
#     twiml= '<Response><Say>Hola amigo comoe estás</Say></Response>',
#     to= '+529661183289',
#     from_ = '+17209243884'
# )

@app.post('/voice')
async def voice():

    response = VoiceResponse()

    response.say('Hola')

    return str(response)
