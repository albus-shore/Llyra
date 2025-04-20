from pathlib import Path
from warnings import warn
import json

### ============================= Inside Functions ============================= ###
## ========================== Name Function ========================== ##
def name(filename:str) -> str:
    '''The function is defined for struct name of model file.
    Args:
        file: A string indicate the name of model file.
    Returns:
        name: A string indicate the name of model file without prefix.
    '''
    # Discriminate whether model file name with prefix
    if filename.endswith('.gguf'):
        name = filename[:-5]
    else:
        name = filename
    # Return model file name value
    return name

## ========================= Folder Function ========================= ##
def folder(directory:str) -> str:
    '''The function is defined for struct directory of model file.
    Args:
        directory: A string indicate the folder of model file placed.
    Returns:
       folder: A string indicate the folder of model file placed with '/'.
    '''
    # Discriminate whether directory of model file end with '/'
    if directory.endswith('/'):
        folder = directory
    else:
        folder = directory + '/'
    # Return model file folder value
    return folder

## =============== Necessary Parameters Check Function =============== ##
def necessary(strategy:str) -> None:
    '''The function is defined for check necessary config parameters
    Args:
        strategy: A string indicate the path to the inference strategy file
    '''
    if not strategy:
        warning = 'Warning: Missing inference strategy file.\n'
        warning += '\t\t Inference unavailiable without manual updating.'
        warn(warning,UserWarning)


### =============================== Expose Class =============================== ###
class Config:
    '''The class is defined for work with the toolkit's configurations.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Config class object.
        Returns:
            config: A object indicate config parameters and operation.
        '''
        # Define default path to config file
        self.config = 'config/config.json'
        # Initialize config attributes
        self.model:str = None
        self.directory:str = None
        self.indicate:dict = {
            'begin': None,
            'end': None,
            }
        self.strategy:str = None
        self.placeholder:dict = {
            'history': None,
            'rag': None,
            'tool': None,
            }
        self.gpu:bool = False
        self.ram:bool = False

    ## ============================= Load Method ============================= ##
    def load(self,path:str=None) -> None:
        '''The method is defined for load toolkit config file.
        Args:
            path: A string indicate the path to the config file.
        '''
        # Discriminate whether changing defualt config file path
        if path:
            self.config = path
        # Load config file
        config_path:object = Path(self.config)
        try:
            config_json:str = config_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            if path:
                error = 'Error: Config file not found in provided path.'
            else:
                error = 'Error: Missing config file.'
            raise FileNotFoundError(error)
        else:
            config_dictionary:dict = json.loads(config_json)
        # Read config parameter
        self.model = config_dictionary.get('model',None)
        self.directory = config_dictionary.get('directory',None)
        if config_dictionary.get('indicate',False):
            self.indicate['begin'] = config_dictionary.get('indicate').get('begin',None)
            self.indicate['end'] = config_dictionary.get('indicate').get('end',None)
        self.strategy = config_dictionary.get('strategy',None)
        if config_dictionary.get('placeholder',False):
            self.placeholder['history'] = config_dictionary.get('placeholder').get('history')
            self.placeholder['rag'] = config_dictionary.get('placeholder').get('rag')
            self.placeholder['tool'] = config_dictionary.get('placeholder').get('tool')
        self.gpu = config_dictionary.get('gpu',None)
        self.ram = config_dictionary.get('ram',None)
        # Critical parameters check
        if not self.model:
            error = 'Error: Missing model file name parameter.'
            raise IndexError(error)
        if not self.directory:
            error = 'Error: Missing model file directory parameter.'
            raise IndexError(error)
        # Necessary parameters check
        necessary(self.strategy)
        # Fix possible invalid attribute
        self.model = name(self.model)
        self.directory = folder(self.directory)
        # Make model file path
        self.path = self.directory + self.model + '.gguf'

    ## ============================ Update Method ============================ ##
    def update(self,
               model:str,directory:str,
               begin:str,end:str,
               strategy:str,
               history:str,rag:str,tool:str,
               gpu:bool,
               ram:bool,) -> None:
        '''The method is defined for update config parameters with inputs.
        Args:
            model: A string indicate the name of model file
            directory: A string indicate the directory of model file
            begin: A string indicate begin of context squence for inference.
            end: A string indicate end of context squence for inference.
            strategy: A string indicate the path to the inference strategy file.
            history: A string indicate the chat history placeholder in chat prompt.
            rag: A string indicate the chat rag content placeholder in chat prompt.
            tool: A string indicate the chat tools placeholder in chat prompt.
            gpu: A boolean indicate whether using GPU for inference acceleration.
            ram: A boolean indicate whether keeping the model loaded in memory
        '''
        # Update parameter according to the input
        ## Update key parameters
        if model:
            self.model = name(model)
        if directory:
            self.directory = folder(directory)
        if model or directory:
            self.path = self.directory + self.model + '.gguf'
        ## Update normal parameter
        if begin != None:
            self.indicate['begin'] = begin
        if end != None:
            self.indicate['end'] = end
        if strategy != None:
            self.strategy = strategy
        if history != None:
            self.placeholder['history'] = history
        if rag != None:
            self.placeholder['rag'] = rag
        if tool != None:
            self.placeholder['tool'] = tool
        if gpu != None:
            self.gpu = gpu
        if ram != None:
            self.ram = ram
        # Necessary parameters check
        necessary(self.strategy)
        
    ## ============================ Write Method ============================ ##
    def write(self) -> None:
        '''The method is defined for writing current config into file.'''
        # Initialize new config file path
        file_path = Path('config/config.json')
        # Discriminate whether the file name has been occupied
        if file_path.exists():
            alarm = "Alarm: There is a existed config.json under '.config/'."
            alarm += "\n\t  This operation will rewrite all content in it."
            alarm += "\n\t  Send 'w' to confirm operation, "
            alarm += "Send 'q' to terminate process."
            while True:
                action = input(alarm)
                if action.lower() == 'w':
                    break
                elif action.lower() == 'q':
                    raise FileExistsError()
                else:
                    print('Invalid command.')
        # Prepare content
        file_content = {
            'model': self.model,
            'directory': self.directory,
            'indicate':{
                'begin': self.indicate['begin'],
                'end': self.indicate['end'],
                },
            'strategy': self.strategy,
            'placeholder': {
                'history': self.placeholder['history'],
                'rag': self.placeholder['rag'],
                'tool': self.placeholder['tool']
                },
            'gpu': self.gpu,
            'ram': self.ram
            }
        file_content = json.dumps(file_content)
        # Write file
        file_path.write_text(file_content)
        # Terminal Information
        print("Current config has been write into '.config/config.json'.")