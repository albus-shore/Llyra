from .basic import Config
from .utils import Model, struct_model_name, struct_path, struct_suffix
from ...errors.configs import ConfigSectionMissingError, ConfigParameterMissingError
from warnings import warn
from pathlib import Path

class LocalConfig(Config):
    '''The class is defined for work with configurations of local inference.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined for initialize LocalConfig class object.'''
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
    def load(self,path:str|Path) -> None:
        '''The method is defined for load config file for local inference.
        Args:
            path: A string or Path instance indicate the path to the config file.
        '''
        # Load config file
        super()._load(path)
        # Extra all local config parameters
        try:
            content:dict = self._content['local']
        except KeyError:
            raise ConfigSectionMissingError('local')
        # Read model config parameters
        ## Extra all model config parameters
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
    def update(self,
               format:str,
               gpu:bool,
               ram:bool,) -> None:
        '''The method is defined for update config parameters with inputs.
        Args:
            format: A sting indicate the format of chat inference's input.
            gpu: A boolean indicate whether using GPU for inference acceleration.
            ram: A boolean indicate whether keeping the model loaded in memory.
        '''        
        if format != '':
            self.format = format
        if gpu != None:
            self.gpu = gpu
        if ram != None:
            self.ram = ram
    