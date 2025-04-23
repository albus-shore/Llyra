from pathlib import Path
from warnings import warn
import json

### ============================= Inside Functions ============================= ###
## ====================== Role Parameter Check Function ====================== ##
def role(role:dict,is_chat:bool,prompt:str=None) -> None:
    '''The function is defined for check strategy prameter role.
    Args:
        role: A dictionary indicate input and output role.
        is_chat: A boolean indicate whether the check is for chat strategy.
        prompt: A string indicate additional prompt for chat inference.
    '''
    if is_chat:
        if not role['prompt'] and prompt:
            error = 'Error: Missing prompt role parameter for chat inference.'
            raise ValueError(error)
        if not role['input']:
            error = 'Error: Missing input role parameter for chat inference.'
            raise ValueError(error)
        if not role['output']:
            error = 'Error: Missing output role parameter for chat inference.'
            raise ValueError(error)
    else:
        if not role['input']:
            warning = 'Warning: Missing input role parameter for call inference.'
            warn(warning,UserWarning)
        if not role['output']:
            warning = 'Warning: Missing output role parameter for call inference.'
            warn(warning,UserWarning)


## =================== Necessary Parameters Check Function =================== ##
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
        # Define iterative chat strategy
        self.chat_prompt:str = None
        self.chat_role = {
            'prompt': None,
            'input': None,
            'output': None
            }
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
                match strategy['type']:
                    case 'call':
                        self.call_role['input'] = strategy.get('role',{}).get('input')
                        self.call_role['output'] = strategy.get('role',{}).get('output')
                        self.call_stop = strategy.get('stop')
                        self.call_tokens = strategy.get('max_token')
                        self.call_temperature = strategy.get('temperature',0)
                        # Necessray parameter check
                        role(self.call_role,False)
                        necessary(self.call_tokens,self.call_stop)
                    case 'chat':
                        prompt_path = strategy.get('prompt',None)
                        if prompt_path:
                            prompt = Path(prompt_path)
                            try:
                                self.chat_prompt = prompt.read_text('utf-8')
                            except FileNotFoundError:
                                error = 'Error: Prompt file not found in provided path.'
                                raise FileNotFoundError(error)
                        self.chat_role['prompt'] = strategy.get('role',{}).get('prompt')
                        self.chat_role['input'] = strategy.get('role',{}).get('input')
                        self.chat_role['output'] = strategy.get('role',{}).get('output')
                        self.chat_stop = strategy.get('stop')
                        self.chat_tokens = strategy.get('max_token')
                        self.chat_temperature = strategy.get('temperature',0)
                        # Key parameter check
                        role(self.chat_role,True,prompt=self.chat_prompt)
                        # Necessray parameter check
                        necessary(self.chat_tokens,self.chat_stop)
            except KeyError:
                raise KeyError('Error: Invalid strategy format.')

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
        necessary(self.call_tokens,self.call_stop)

    def chat(self,
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
        if prompt != None:
            self.chat_prompt = prompt
        if prompt_role:
            self.chat_role['prompt'] = prompt_role
        if input_role:
            self.chat_role['input'] = input_role
        if output_role:
            self.chat_role['output'] = output_role
        if stop != None:
            self.chat_stop = stop
        if max_token != None:
            self.chat_tokens = max_token
        if temperature != None:
            self.chat_temperature = temperature
        # Necessary Parameter Check
        necessary(self.chat_tokens,self.chat_stop)