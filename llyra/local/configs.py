from warnings import warn
from ..base import Config

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

## =============== Necessary Parameters Check Function =============== ##
def check_necessary(strategy:str,format:str) -> None:
    '''The function is defined for check necessary config parameters.
    Args:
        strategy: A string indicate the path to the inference strategy file.
        format: A sting indicate the format of chat inference's input.
    '''
    if not strategy:
        warning = 'Warning: Missing inference strategy file.\n'
        warning += '\t\t Inference unavailiable without manual updating.'
        warn(warning,UserWarning)
    if not format:
        warning = 'Warning: Missing chat format.\n'
        warning += '\t\t Chat inference may unavailiable '
        warning += "when chat format not contain in model's metadate "
        warning += "or not manual updating."
        warn(warning,UserWarning)


### =============================== Expose Class =============================== ###
class ConfigLocal(Config):
    '''The class is defined for work with configurations of local inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize ConfigLocal class object.'''
        # Initialize parent class
        super().__init__()
        # Define config attributes
        self.model:str = None
        self.directory:str = None
        self.strategy:str = None
        self.format:str = None
        self.gpu:bool = None
        self.ram:bool = None
        # Define path attribute
        self.path:str = None

    ## ============================= Load Method ============================= ##
    def load(self,path:str=None) -> None:
        '''The method is defined for load config file for local inference.
        Args:
            path: A string indicate the path to the config file.
        '''
        # Load config file
        super()._load(path=path)
        # Read config parameter
        self.model = self._config.get('model',None)
        self.directory = self._config.get('directory',None)
        self.strategy = self._config.get('strategy',None)
        self.format = self._config.get('format',None)
        self.gpu = self._config.get('gpu',False)
        self.ram = self._config.get('ram',False)
        # Critical parameters check
        if not self.model:
            error = 'Error: Missing model file name parameter.'
            raise IndexError(error)
        if not self.directory:
            error = 'Error: Missing model file directory parameter.'
            raise IndexError(error)
        # Necessary parameters check
        check_necessary(self.strategy,self.format)
        # Fix possible invalid attribute
        self.model = name(self.model)
        self.directory = super().path(self.directory)
        # Make model file path
        self.path = self.directory + self.model + '.gguf'

    ## ============================ Update Method ============================ ##
    def update(self,
               model:str,
               directory:str,
               strategy:str,
               format:str,
               gpu:bool,
               ram:bool,) -> None:
        '''The method is defined for update config parameters with inputs.
        Args:
            model: A string indicate the name of model file.
            directory: A string indicate the directory of model file.
            strategy: A string indicate the path to the inference strategy file.
            format: A sting indicate the format of chat inference's input.
            gpu: A boolean indicate whether using GPU for inference acceleration.
            ram: A boolean indicate whether keeping the model loaded in memory.
        '''
        # Update parameter according to the input
        ## Update key parameters
        if model:
            self.model = name(model)
        if directory:
            self.directory = super().path(directory)
        if model or directory:
            self.path = self.directory + self.model + '.gguf'
        ## Update normal parameter
        if strategy != None:
            self.strategy = strategy
        if format != None:
            self.format = format
        if gpu != None:
            self.gpu = gpu
        if ram != None:
            self.ram = ram
        # Necessary parameters check
        check_necessary(self.strategy,self.format)
        
    ## ============================ Write Method ============================ ##
    def write(self) -> None:
        '''The method is defined for writing current config into file.'''
        # Prepare content
        content = {
            'model': self.model,
            'directory': self.directory,
            'strategy': self.strategy,
            'format': self.format,
            'gpu': self.gpu,
            'ram': self.ram
            }
        super()._write(content=content)