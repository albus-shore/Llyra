from pathlib import Path
from warnings import warn
import json

### ============================= Inside Functions ============================= ###
## =============== Necessary Parameters Check Function =============== ##
def necessary(max_token:int,stop:str) -> None:
    '''The function is defined for check necessary strategy parameters.
    Args:
        stop: A string indicate where the model should stop generation.
        max_token: A integrate indicate 
            the max token number of model generation.
    '''
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
                    self.call_stop = strategy['stop']
                    self.call_tokens = strategy['max_token']
                    self.call_temperature = strategy['temperature']
                elif strategy['type'] == 'chat':
                    pass
            except KeyError:
                raise KeyError('Error: Invalid strategy formate.')
        # Critial parameter check
        if not self.call_role['input']:
            raise ValueError('Error: Missing input role parameter.')
        if not self.call_role['output']:
            raise ValueError('Error: Missing output role parameter.')
        # Necessray parameter check
        necessary(self.call_tokens,self.call_stop)

                
    ## ========================== Update Methods ========================== ##
    def call(self,
             input_role:str,output_role:str,
             stop:str,max_token:int,
             temperature:float) -> None:
        '''The method is defined for update inference strategy for call.
        Args:
            input_roleinput_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        if input_role:
            self.call_role['input'] = input_role
        if output_role:
            self.call_role['output'] = output_role
        if stop != None:
            self.call_stop = stop
        if max_token != None:
            self.call_tokens = max_token
        if temperature != None:
            self.call_temperature = temperature
        # Necessray parameter check
        necessary(self.call_tokens,self.call_stop)
