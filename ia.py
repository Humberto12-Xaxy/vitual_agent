import openai
import json
import os
from dotenv import load_dotenv

class IA:

    def __init__(self) -> None:
        load_dotenv()        
        openai.api_key = os.getenv('API_KEY')

    
    def process_funtions(self, text):

        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo-0613',
            messages = [
                {'role': 'system', 'content': 'Eres un agente telefónico de call center que trabaja como soporte para la empresa de IZZI'},
                {'role': 'system', 'content': text}, 
            ],
            functions = [
                {
                    'name' : 'no_internet_service',
                    'description' : 'Dar intrucciones para arreglar el problema de internet',
                    'parameters' : {
                        'type': 'object',
                        'properties' : {
                             'instruciones' : {                               
                                'type' : 'string',
                                'description' : 'Dar instrucciones que ayuden a resolver los problemas de internet, recuerda que eres de soporte tecnico'
                            }
                        },
                    },
                },
                {
                    'name' : 'bye',
                    'description' : 'Despedirce del cliente',
                    'parameters' : {
                        'type' : 'object',
                        'properties': {
                            'despedida' : {
                                'type' : 'string',
                                'description' : 'Despedirse del cliente cuando ya hayas dado la información que el requrió'
                            }
                        }
                    }
                }
            ],
            function_call = 'auto'
        )

        message:dict = response['choices'][0]['message']

        if message.get('function_call'):
            function_name = message['function_call']['name']
            args = message['function_call']['arguments']
            
            args = json.loads(args)
            return function_name, args, message
        
        return None, None, message

    def process_response(self, text, message, function_name, function_response):

        if function_name != '':
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages = [
                    {'role' : 'system', 'content' : 'Eres un agente telefónIco de call center que trabaja para la empresa de IZZI'},
                    {'role' : 'user', 'content' : text},
                    message,
                    {
                        'role' : 'function',
                        'name' : function_name,
                        'content' : function_response
                    },
                ],
            )

            return response['choices'][0]['message']['content']
        
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages = [
                    {'role' : 'system', 'content' : 'Eres un agente telefónico de call center que trabaja para la empresa de IZZI'},
                    {'role' : 'user', 'content' : text},
                ],
            )

            return response['choices'][0]['message']['content']