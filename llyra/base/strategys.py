from pathlib import Path
import json

### ============================== Internal Class ============================== ###
## =============================== Call Class =============================== ##
class _Call:
    '''The class is defined for work with strategies with
        universal single call inference.'''
    def __init__(self) -> None:
        '''The method is defined for initializing internal Call class object.'''
        pass

## =============================== Chat Class =============================== ##
class _Chat:
    '''The class is defined for work with strategies with
        universal iterative chat inference.'''
    def __init__(self) -> None:
        '''The method is defined for initializing internal Chat class object.'''
        self.prompt:str = None
        self.role = {
            'prompt': None,
            'input': None,
            'output': None,
            }
    
    def load(self,strategy:dict) -> None:
        '''The method is defined for loading universal strategies from file.
        Args:
            strategy: A dictionary indicate content of universal strategies.
        '''
        path = strategy.get('prompt',None)
        if path:
            prompt = Path(path)
            try:
                self.prompt = prompt.read_text('utf-8')
            except FileNotFoundError:
                error = 'Error: Prompt file not found in provided path.'
                raise FileNotFoundError(error)
        self.role['prompt'] = strategy.get('role',{}).get('prompt',None)
        self.role['input'] = strategy.get('role',{}).get('input',None)
        self.role['output'] = strategy.get('role',{}).get('output',None)
        self._check_role()

    def update(self,prompt:str,
               prompt_role:str,input_role:str,output_role:str) -> None:
        '''The method is defined for update universal strategies from file.
        Args:
            prompt: A string indicate additional prompt for chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
        '''
        if prompt != None:
            self.prompt = prompt
        if prompt_role != None:
            self.role['prompt'] = prompt_role
        if input_role:
            self.role['input'] = input_role
        if output_role:
            self.role['output'] = output_role
        self._check_role()

    def _check_role(self) -> None:
        '''The method is defined for check attribute role.'''
        if not self.role['prompt'] and self.prompt:
            error = 'Error: Missing prompt role parameter for chat inference.'
            raise ValueError(error)
        if not self.role['input']:
            error = 'Error: Missing input role parameter for chat inference.'
            raise ValueError(error)
        if not self.role['output']:
            error = 'Error: Missing output role parameter for chat inference.'
            raise ValueError(error)
        
### =============================== Expose Class =============================== ###
class Strategy:
    '''The class is defined to define basic attributes and internal methods,
    for working with inference strategies.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initalizeing Strategy class object.'''
        # Initialize necessary object attributes
        self.call = _Call()
        self.chat = _Chat()

    ## ============================= Load Method ============================= ##
    def _load(self,path:str,call,chat) -> None:
        '''The method is defined for loading strategy content from file.
        Args:
            path: A string indicate the path to the strategy file.
            call: A function indicate how to load strategies of single call .
            chat: A function indicate how to load strategies of iterative chat.
        '''
        # Discriminate whether getting path input
        if path:
            file = Path(path)
        else:
            return
        # Load strategy file
        try:
            content = file.read_text(encoding='utf-8')
        except FileNotFoundError:
            error = 'Error: Strategy file not found in provided path.'
            raise FileNotFoundError(error)
        else:
            strategys = json.loads(content)
            if type(strategys) != list:
                error = 'Error: Stratgy should be a list.'
                raise IsADirectoryError(error)
        # Read strategy
        for strategy in strategys:
            try:
                match strategy['type']:
                    case 'call':
                        call(strategy)
                    case 'chat':
                        self.chat.load(strategy)
                        chat(strategy)
            except KeyError:
                raise KeyError('Error: Invalid strategy format.')                
