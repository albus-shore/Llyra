from warnings import warn
from ..base import Strategy

### ============================= Inside Functions ============================= ###
## ====================== Role Parameter Check Function ====================== ##
def role(role:dict) -> None:
    '''The function is defined for check strategy prameter role.
    Args:
        role: A dictionary indicate input and output role.
    '''
    if not role['input']:
        warning = 'Warning: Missing input role parameter for call inference.'
        warn(warning,UserWarning)
    if not role['output']:
        warning = 'Warning: Missing output role parameter for call inference.'
        warn(warning,UserWarning)


## =================== Necessary Parameters Check Function =================== ##
def check_necessary(max_token:int,stop:str) -> None:
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
class StrategyLocal(Strategy):
    '''The class is defind for work with inference strategies of local inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize StrategyLocal class object.'''
        # Initialize parent class
        super().__init__()
        # Define single call strategy
        self.call.role = {
            'input': None,
            'output': None
            }
        self.call.stop = None
        self.call.tokens = None
        self.call.temperature = None
        # Define iterative chat strategy
        self.chat.stop = None
        self.chat.tokens = None
        self.chat.temperature = None

    ## ============================= Load Method ============================= ##
    def load(self,path:str) -> None:
        '''The method is defined for load strategy file for local inference.
        Args:
            path: A string indicate the path to the strategy file.
        '''
        # Define strategy loading method
        def call(strategy:dict):
            self.call.role['input'] = strategy.get('role',{}).get('input')
            self.call.role['output'] = strategy.get('role',{}).get('output')
            self.call.stop = strategy.get('stop')
            self.call.tokens = strategy.get('max_token')
            self.call.temperature = strategy.get('temperature',0)
            role(self.call.role)
            check_necessary(self.call.tokens,self.call.stop)
        def chat(strategy:dict):
            self.chat.stop = strategy.get('stop')
            self.chat.tokens = strategy.get('max_token')
            self.chat.temperature = strategy.get('temperature',0)
            check_necessary(self.chat.tokens,self.chat.stop)
        # Load strategy
        super()._load(path,call,chat)

    ## ========================== Update Methods ========================== ##
    def update_call(self,
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
            self.call.role['input'] = input_role
        if output_role != None:
            self.call.role['output'] = output_role
        if stop != None:
            self.call.stop = stop
        if max_token != None:
            self.call.tokens = max_token
        if temperature != None:
            self.call.temperature = temperature
        # Necessray parameter check
        check_necessary(self.call.tokens,self.call.stop)

    def update_chat(self,
             prompt:str,
             prompt_role:str,input_role:str,output_role:str,
             stop:str,max_token:int,
             temperature:float) -> None:
        '''The method is defined for update inference strategy for chat.
        Args:
            prompt: A string indicate additional prompt for chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        self.chat.update(prompt,
                         prompt_role,input_role,output_role)
        if stop != None:
            self.chat.stop = stop
        if max_token != None:
            self.chat.tokens = max_token
        if temperature != None:
            self.chat.temperature = temperature
        # Necessary Parameter Check
        check_necessary(self.chat.tokens,self.chat.stop)