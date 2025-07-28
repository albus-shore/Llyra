from .basic import Config
from .utils import Model, struct_model_name, struct_path, struct_suffix
from ...exceptions.components.configs import ConfigSectionMissingError, ConfigParameterMissingError
from ...exceptions.components.configs import ConfigModelNotCompatibleError
from warnings import warn
from pathlib import Path

class LocalConfig(Config):
    '''The class is defined to work with configurations of local inference.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined to initialize LocalConfig class object.'''
        # Initialize parent class
        super().__init__()
        # Define config attributes
        self.model:Model = None
        self.format:str = None
        self.gpu:bool = None
        self.ram:bool = None
        # Define path attribute
        self.path:str = None

    ## ================================ Load Method ================================ ##
    def load_toml(self,path:str|Path) -> None:
        '''The method is defined to load config file for local inference.
        Args:
            path: A string or Path instance indicate the path to the config file.
        '''
        # Load config file
        super()._load(path)
        # Extract all local config parameters
        try:
            content:dict = self._content['local']
        except KeyError:
            raise ConfigSectionMissingError('local')
        # Read model config parameters
        ## Extract all model config parameters
        try:
            model = content['model']
        except KeyError:
            raise ConfigSectionMissingError('local.model')
        ## Read model config parameters
        try:
            name = model['name']
        except KeyError:
            raise ConfigParameterMissingError('local.model','name')
        else:
            name = struct_model_name(name)
        try:
            directory = model['directory']
        except KeyError:
            raise ConfigParameterMissingError('local.model','directory')
        else:
            directory = struct_path(directory)
        try:
            suffix = model['suffix']
        except KeyError:
            raise ConfigParameterMissingError('local.model','suffix')
        else:
            suffix = struct_suffix(suffix)
        self.model:Model = Model(name,directory,suffix)
        # Read environment config parameters
        try:
            self.format = content['format']
        except KeyError:
            message = 'Missing `format` parameter of `local` section in `config.toml`'
            message += ' , auto-fallback to `None`.'
            warn(message,RuntimeWarning)
            self.format = None
        try:
            self.gpu = content['gpu']
        except KeyError:
            message = 'Missing `gpu` parameter of `local` section in `config.toml`'
            message += ' , auto-fallback to `False`.'
            warn(message,RuntimeWarning)
            self.gpu = False
        try:
            self.ram = content['ram']
        except KeyError:
            message = 'Missing `ram` parameter of `local` section in `config.toml`'
            message += ' , auto-fallback to `False`.'
            warn(message,RuntimeWarning)
            self.ram = False
        # Make model file path
        self.path = self.model.directory + self.model.name + self.model.suffix

    ## =============================== Update Method =============================== ##
    def update_parameter(self,
                         format:str,
                         gpu:bool,
                         ram:bool,) -> None:
        '''The method is defined to update config parameters with inputs.
        Args:
            format: A string indicate the format of chat inference's input.
            gpu: A boolean indicate whether using GPU for inference acceleration.
            ram: A boolean indicate whether keeping the model loaded in memory.
        '''        
        if format != '':
            self.format = format
        if gpu != None:
            self.gpu = gpu
        if ram != None:
            self.ram = ram
    
    ## ============================== Validate Method ============================== ##
    def validate_model(self,model:str) -> None:
        '''The method is defined to validate 
        whether the claiming model is compatible with the current config.
        Args:
            model: A string indicate the name of claiming model for inference.
        '''
        try:
            assert self.model.name == model
        except AssertionError:
            raise ConfigModelNotCompatibleError(config=self.model.name,claiming=model)