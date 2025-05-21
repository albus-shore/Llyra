from .configs import ConfigRemote
from .strategys import StrategyRemote
from .prompts import PromptRemote
from .logs import LogRemote
import requests

class Remote:
    '''The class is defined for fulfill remote LLM call.'''
    ## ========================= Class Initialize Method ========================== ##
    def __init__(self,path:str=None) -> None:
        '''The method is defined for initialize Local class object.
        Args:
            path: A string indicate the path to config file.
        '''
        # Initialize necessary object attributes
        self.config = ConfigRemote()
        self.strategy = StrategyRemote()
        self.prompt = PromptRemote()
        self.log = LogRemote()
        # Import toolkit config
        self.config.load(path)
        # Import inference config
        self.strategy.load(self.config.strategy)
        # Test connection to Ollama server
        url = self.config.url + self.config.endpoint + 'version'
        try:
            test = requests.get(url=url)
            test_return = test.json()
        except requests.RequestException:
            error = 'Error: Connect to server failed.'
            raise ConnectionError(error)
        else:
            if 'version' not in test_return:
                error = 'Error: Not supported service.'
                raise ConnectionError(error)
        # Initialize current inference attributea
        self.query:str
        self.response:str

    def call(self,message:str,
             system:str=None,
             stop:str=None,temperature:float=None) -> str:
        '''The method is defined for fulfill single LLM call.
        Args:
            message: A string indicate the input content for chat inference.
            system: A string indicate system prompt for model inference.
            stop: A string indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model reponse content.
        '''
        # Get input content
        self.query = message
        # Update inference strategy if necessary
        self.strategy.update_call(system,stop,temperature)
        # Make options
        options = {}
        if self.strategy.call.stop:
            options['stop'] = self.strategy.call.stop
        if self.strategy.call.temperature:
            options['temperature'] = self.strategy.call.temperature
        # Make prompt
        prompt = self.prompt.call(self.query)
        # Make request body
        body = {
            'model': self.config.model,
            'prompt': prompt,
            'stream': False
            }
        if self.strategy.call.system:
            body['system'] = self.strategy.call.system    
        if options:
            body['options'] = options
        # Fulfill request
        url = self.config.url + self.config.endpoint + 'generate'
        try:
            response = requests.post(url,json=body)
            response_content = response.json()
        except requests.RequestException:
            raise ConnectionError('Error: Remote inference failed.')
        else:
            self.response = response_content['response']
        # Update log
        self.log.call(self.config.model,self.query,self.response)
        # Return model inference response
        return self.response

    def chat(self,message:str,keep:bool,
             *iteration,addition:str=None,
             prompt_role:str=None,input_role:str=None,output_role:str=None,
             stop:str=None,temperature:str=None) -> str:
        '''The method is defined for fulfill iterative chat inference.
        Args:
            message: A string indicate the input content for chat inference.
            keep: A string indicate whether continue last chat iteration.
            iteration: A list of dictionaries contain 
                additional iteration history for the iterative chat inference.
            addition: A string indicate additional prompt 
                for the iterative chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model response content of the chat inference.
        '''
        # Get input content
        self.query = message
        # Update inference strategy if necessary
        self.strategy.update_chat(addition,
                                  prompt_role,input_role,output_role,
                                  stop,temperature)
        # Clear prompt iteration record if necessary
        self.prompt.iterate(None,None,keep)
        # Add additional prompt iteration record if necessary
        if iteration:
            self.prompt._iteration.extend(iteration)
        # Make options
        options = {}
        if self.strategy.chat.stop:
            options['stop'] = self.strategy.chat.stop
        if self.strategy.chat.temperature:
            options['temperature'] = self.strategy.chat.temperature
        # Make prompt
        prompt = self.prompt.chat(self.strategy.chat.role,
                                  self.query,
                                  self.strategy.chat.prompt)
        # Make request body
        body = {
            'model': self.config.model,
            'messages': prompt,
            'stream': False
            }
        if options:
            body['options'] = options
        # Fulfill request    
        url = self.config.url + self.config.endpoint + 'chat'
        try:
            response = requests.post(url,json=body)
            response_content = response.json()
        except requests.RequestException:
            raise ConnectionError('Error: Remote inference failed.')
        else:
            self.response = response_content['message']['content']
        # Update prompt iteration record
        self.prompt.iterate(self.strategy.chat.role['input'],self.query,True)
        self.prompt.iterate(self.strategy.chat.role['output'],self.response,True)
        # Update log
        self.log.chat(model=self.config.model,
                      prompt=self.strategy.chat.prompt,
                      role=self.strategy.chat.role,
                      input=self.query,output=self.response,
                      keep=keep)
        # Return model inference response
        return self.response