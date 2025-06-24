import requests
from .utils import convert_str2list
from ....errors.remotes import RemoteServerConnectionError, RemoteServiceNotCompatibleError, RemoteModelNotAvailableError, RemoteServiceError

class Ollama:
    '''The class is defined for abstract basic methods 
    for remote backend of Ollama service.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,url:str,model:str) -> None:
        '''The method is defined for initialize Ollama class object.
        Args:
            url: A string indicate the url of ollama server before specific interface.
            model: A string indicate the name of model for inference.
        '''
        # Test service availability
        try:
            test = requests.get(url=url+'tags')
        except requests.RequestException:
            raise RemoteServerConnectionError()
        try:
            response_content = test.json()
            available_models = response_content['models']
            model_names = [available_model['name'] 
                for available_model in available_models]
        except (requests.RequestException, KeyError):
            raise RemoteServiceNotCompatibleError()
        if model not in model_names:
            raise RemoteModelNotAvailableError(model)
        # Get input attributes
        self.url = url
        self.model = model

    ## ============================= Inference Methods ============================= ##
    def call(self,prompt:str,stop:str|list,temperature:float) -> str:
        '''The method is defined for fulfill single call inference.
        Args:
            prompt: A string indicate the content for model inference.
            stop: A string or a list of strings 
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model response content.
        '''
        # Make options
        options = {
            'stop': convert_str2list(stop),
            'temperature': temperature
            }
        # Make request body
        body = {
            'model': self.model,
            'prompt': prompt,
            'stream': False,
            'options': options,
            }
        # Execute remote inference
        call = requests.post(url=self.url+'generate',
                             json=body,
                             stream=False)
        response_content = call.json()
        # Extract response string
        try:
            response = response_content['response']
        except KeyError:
            raise RemoteServiceError(response_content['error'])
        # Return remote inference response
        return response
    
    def chat(self,prompt:list,stop:str|list,temperature:float) -> str:
        '''The method is defined for fulfill single call inference.
        Args:
            prompt: A list indicate proper structed content for chat inference.
            stop: A string or a list of strings 
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model response content.
        '''
        # Make options
        options = {
            'stop': convert_str2list(stop),
            'temperature': temperature
            }
        # Make request body
        body = {
            'model': self.model,
            'messages': prompt,
            'stream': False,
            'options': options,
            }
        # Execute remote inference
        chat = requests.post(url=self.url+'chat',
                             json=body,
                             stream=False)
        response_content = chat.json()
        # Extract response string
        try:
            response_message = response_content['message']
        except KeyError:
            raise RemoteServiceError(response_content['error'])
        else:
            response = response_message['content']
        # Return remote inference response
        return response