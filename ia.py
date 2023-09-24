import openai
import json
import os
from dotenv import load_dotenv

from instructions import Instruction

class IA:

    def __init__(self) -> None:
        load_dotenv()        
        openai.api_key = os.getenv('API_KEY')
        self.instruction = Instruction()
        self.no_internet_service = json.dumps({'instruction' : self.instruction.no_internet_service()})

    
    def process_funtions(self, text):

        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo-0613',
            messages = [
                {'role': 'system', 'content': 'Eres un agente telefónico de call center que trabaja como soporte para la empresa de IZZI, No puedes contar chistes ya que no eres un payaso'},
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
                    'name' : 'farewell',
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
                },
                {
                    'name' : 'stop',
                    'description' : 'Disculpa, necesito hacer una interripción',
                    'parameters' : {
                        'type' : 'object',
                        'properties' : {
                            'interrumpirse' : {
                                'type' : 'string',
                                'description':'Verifica cuando haya una señal de interrupción'
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

    def process_response(self, text, message, function_name, function_response = ''):
        if function_name == 'no_internet_service':
            function_response = self.no_internet_service

        if function_name != '':
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages = [
                    {'role' : 'system', 'content' : 'Eres un agente telefónico de call center que trabaja como soporte para la empresa de IZZI, No puedes contar chistes ya que no eres un payaso'},
                    {'role' : 'user', 'content' : text},
                    message,
                    {
                        'role' : 'function',
                        'name' : function_name,
                        'content' : function_response
                    },
                ],
            temperature = 0.7
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
        
        

    def call_intro(self):

        instruction = 'Comienza la llamada con un saludo no digas al principio "agente telefonico", di que eres un bot'

        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages = [
                    {'role' : 'system', 'content' : 'Eres un agente telefónico de call center que trabaja para la empresa de IZZI'},
                    {'role' : 'user', 'content' : instruction},
                ],
            )
        return response['choices'][0]['message']['content']
    

    def conversarion(self, conversation:list):

        response =  openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages = conversation
            )
        
        return response['choices'][0]['message']['content']


if __name__ == '__main__':

    ia = IA()

    print(ia.call_intro())
