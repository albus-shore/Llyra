from pathlib import Path
from warnings import warn
import json

### ============================= Inside Functions ============================= ###
## ========================== Name Function ========================== ##
def name(file:str) -> str:
    '''The function is defined for struct name of model file.
    Args:
        file: A string indicate the name of model file.
    Returns:
        name: A string indicate the name of model file without prefix.
    '''
    # Discriminate whether model file name with prefix
    if file.endswith('.gguf'):
        name = file[:-5]
    else:
        name = file
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


### =============================== Expose Class =============================== ###
class Config:
    '''The class is defined for work with the toolkit's configurations.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Config class object.
        Returns:
            config: A object indicate config parameters and operation.
        '''
        self.config = 'config/config.json'

    ## ========================== Load Method ========================== ##
    def load(self,path:str=None) -> None:
        '''The method is defined for load toolkit config file.
        Args:
            path: A string indicate the path to the config file.
        '''
        # Define config attributes
        self.attributes = ('model',
                      'directory',
                      'strategy',
                      'gpu',
                      'format',
                      'ram',
                      'path',)
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
            for attribute in self.attributes:
                setattr(self,attribute,config_dictionary.get(attribute))
            # Critical parameters check
            if not self.model:
                error = 'Error: Missing model file name parameter.'
                raise IndexError(error)
            if not self.directory:
                error = 'Error: Missing model file directory parameter.'
                raise IndexError(error)
            # Necessary parameters check
            if not self.strategy:
                warning = 'Warning: Missing inference strategy file.\n'
                warning += '\t\t Inference unavailiable without manual updating.'
                warn(warning,UserWarning)
            if not self.format:
                warning = 'Warning: Missing chat format.'
                warning += '\t\t Chat inference unavailiable without manual updating'
                warn(warning,UserWarning)
            # Fix possible invalid attribute
            self.model = name(self.model)
            self.directory = folder(self.directory)
            # Make model file path
            self.path = self.directory + self.model + '.gguf'
        
    ## ========================== Update Method ========================== ##