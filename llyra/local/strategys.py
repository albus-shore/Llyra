from pathlib import Path
from warnings import warn
import json

### ============================= Inside Functions ============================= ###
## =============== Necessary Parameters Check Function =============== ##
def necessary(input_role,output_role,max_token:int,stop:str) -> None:
    '''The function is defined for check necessary strategy parameters.
    Args:
        input_role: A string indicate the role of input.
        output_role: A string indicate the role of output.
        stop: A string indicate where the model should stop generation.
        max_token: A integrate indicate 
            the max token number of model generation.
    '''
    if not input_role:
        warning = 'Warning: Error set input role indicate token, '
        warning += 'model inference may not behave properly.'
        warn(warning,UserWarning)
    if not output_role:
        warning = 'Warning: Error set output role indicate token, '
        warning += 'model inference may not behave properly.'
        warn(warning,UserWarning)
    if not max_token:
        warning = 'Warning: Error set max token strategy parameter, '
        warning += 'the max generation token number will be set '
        warning += 'refer to the loaded model.'
        warn(warning,UserWarning)
    if not stop:
        warning = 'Warning: Missing stop strategy parameter, '
        warning += "inference won't stop "
        warning += "until max generation token number reached."
        warn(warning,UserWarning)


### =============================== Expose Class =============================== ###
class Strategy:
    '''The class is defind for work with model inference strategies.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Strategy class object.
        Returns:
            strategy: A object indicate inference strategy.
        '''
        # Define single call strategy
        self.call_role = {
            'input': None,
            'output': None
            }
        self.call_stop:str = None
        self.call_tokens:int = None
        self.call_temperature:float = None
        # Define iteration chat strategy
        self.chat_role = {
            'input': None,
            'output': None
            }
        self.chat_prompt:str = None
        self.chat_stop:str = None
        self.chat_tokens:int = None
        self.chat_temperature:float = None

    ## ============================= Load Method ============================= ##
    def load(self,path:str) -> None:
        '''The method is defined for load inference strategy file.
        Args:
            path: A string indicate the path to the strategy file.
        '''
        # Discriminate whether getting path input
        if path:
            file_path = Path(path)
        else:
            return
        # Load strategy file
        try:
            file_content = file_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            error = 'Error: Strategy file not found in provided path.'
            raise FileNotFoundError(error)
        else:
            strategys = json.loads(file_content)
            if type(strategys) != list:
                error = 'Error: Stratgy should be a list.'
                raise IsADirectoryError(error)
        # Read strategy
        for strategy in strategys:
            try:
                if strategy['type'] == 'call':
                    self.call_role['input'] = strategy['role']['input']
                    self.call_role['output'] = strategy['role']['output']
                    self.call_stop = strategy['stop'] or ''
                    self.call_tokens = strategy['max_token']
                    self.call_temperature = strategy['temperature']
                elif strategy['type'] == 'chat':
                    self.chat_role['input'] = strategy['role']['input']
                    self.chat_role['output'] = strategy['role']['output']
                    if strategy.get('prompt',False):
                        chat_prompt_path = Path(strategy['prompt'])
                        try:
                            chat_prompt = chat_prompt_path.read_text('utf-8')
                        except FileNotFoundError:
                            error = 'Error: Prompt file not found.'
                            raise FileNotFoundError(error)
                        else:
                            self.chat_prompt = chat_prompt
                    self.chat_stop = strategy['stop'] or ''
                    self.chat_tokens = strategy['max_token']
                    self.chat_temperature = strategy['temperature']
            except KeyError:
                raise KeyError('Error: Invalid strategy formate.')
        # Necessray parameter check
        if self.call_temperature != None:
            necessary(self.call_role['input'],self.call_role['output'],
                      self.call_tokens,self.call_stop)
        if self.chat_temperature != None:
            necessary(self.chat_role['input'],self.chat_role['output'],
                      self.chat_tokens,self.chat_stop)

                
    ## ========================== Update Methods ========================== ##
    def call(self,
             input_role:str,output_role:str,
             stop:str,max_token:int,
             temperature:float) -> None:
        '''The method is defined for update inference strategy for call.
        Args:
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        if input_role != None:
            self.call_role['input'] = input_role
        if output_role != None:
            self.call_role['output'] = output_role
        if stop != None:
            self.call_stop = stop
        if max_token != None:
            self.call_tokens = max_token
        if temperature != None:
            self.call_temperature = temperature
        # Necessray parameter check
        necessary(self.call_role['input'],self.call_role['output'],
                  self.call_tokens,self.call_stop)
        if self.call_temperature == None:
            error = 'Error: Inference temperature must be set.'
            raise ValueError(error)

    def chat(self,
             prompt:str,
             input_role:str,output_role:str,
             stop:str,max_token:int,
             temperature:float) -> None:
        '''The method is defined for update inference strategy for chat.
        Args:
            prompt: A string indicate the prompt of iterative chat inference.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        if prompt != None:
            self.chat_prompt = prompt
        if input_role != None:
            self.chat_role['input'] = input_role
        if output_role != None:
            self.chat_role['output'] = output_role
        if stop != None:
            self.chat_stop = stop
        if max_token != None:
            self.chat_tokens = max_token
        if temperature != None:
            self.chat_temperature = temperature
        # Necessray parameter check
        necessary(self.chat_role['input'],self.chat_role['output'],
                  self.chat_tokens,self.chat_stop)
        if self.chat_temperature == None:
            error = 'Error: Inference temperature must be set.'
            raise ValueError(error)
