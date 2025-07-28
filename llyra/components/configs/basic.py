import tomllib
from pathlib import Path
from warnings import warn
from sqlmodel import create_engine
from ...exceptions.components.configs import ConfigSectionMissingError, ConfigParameterMissingError

class Config:
    '''The class is defined to define basic attributes and internal methods, 
        for working with configurations.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined to initialize Config class object.'''
        # Define global config attribute
        self.strategy:Path = None
        self.logbase = create_engine('sqlite://')
        # Define assistant internal attribute
        self._path:Path = Path('configs/config.toml')
        self._content:dict = None

    ## =========================== Internal Load Method =========================== ##
    def _load(self,path:str|Path) -> dict:
        '''The method is defined to load config from default or custom path.
        Args:
            path: A string or Path instance 
                indicate the custom path to the config file.
        '''
        # Discriminate whether loading from custom path or default path
        if path:
            if type(path) == Path:
                self._path = path
            else:
                self._path:Path = Path(path)
        # Load config file content
        try:
            with self._path.open('rb') as obj:
                self._content = tomllib.load(obj)
        except FileNotFoundError:
            if path:
                error = 'Config file not found in provided path.'
            else:
                error = 'Missing config file.'
            raise FileNotFoundError(error)
        # Extract all global config parameters
        try:
            content = self._content['global']
        except KeyError:
            raise ConfigSectionMissingError('global')
        # Read strategy config parameter
        try:
            strategy = content['strategy']
        except KeyError:
            raise ConfigParameterMissingError('global','strategy')
        else:
            self.strategy:Path = Path(strategy)
        # Read logbase config parameter
        try:
            logbase = content['logbase']
        except KeyError:
            message = 'Missing `logbase` parameter of `global` section in `config.toml`'
            message += ' , auto-fallback to `sqlite://` for in-memory database.'
            warn(message,RuntimeWarning)
        else:
            self.logbase = create_engine(url=logbase)