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
def necessary(strategy:str,format:str) -> None:
    '''The function is defined for check necessary config parameters
    Args:
        strategy: A string indicate the path to the inference strategy file
        format: A sting indicate the format of chat inference's input
    '''
    if not strategy:
        warning = 'Warning: Missing inference strategy file.\n'
        warning += '\t\t Inference unavailiable without manual updating.'
        warn(warning,UserWarning)
    if not format:
        warning = 'Warning: Missing chat format.'
        warning += '\t\t Chat inference unavailiable without manual updating'
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
        # Define config attributes
        self.attributes = ('model',
                      'directory',
                      'strategy',
                      'gpu',
                      'format',
                      'ram',
                      'path',)

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
        necessary(self.strategy,
                  self.format)
        # Fix possible invalid attribute
        self.model = name(self.model)
        self.directory = folder(self.directory)
        # Make model file path
        self.path = self.directory + self.model + '.gguf'

    ## ============================ Update Method ============================ ##
    def update(self,
               model:str,
               directory:str,
               strategy:str,
               gpu:bool,
               format:str,
               ram:bool,) -> None:
        '''The method is defined for update config parameters with inputs.
        Args:
            model: A string indicate the name of model file
            directory: A string indicate the directory of model file
            strategy: A string indicate the path to the inference strategy file
            gpu: A boolean indicate whether using GPU for inference acceleration
            format: A sting indicate the format of chat inference's input
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
        input_config = (strategy,
                        gpu,
                        format,
                        ram)
        normal_config = self.attributes[2:-1]
        for value in input_config:
            if value != None:
                index = input_config.index(value)
                attribute = normal_config[index]
                setattr(self,attribute,value)
        # Necessary parameters check
        necessary(self.strategy,
                  self.format)
        
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
            'strategy': self.strategy,
            'gpu': self.gpu,
            'format': self.format,
            'ram': self.ram
            }
        file_content = json.dumps(file_content)
        # Write file
        file_path.write_text(file_content)
        # Terminal Information
        print("Current config has been write into '.config/config.json'.")