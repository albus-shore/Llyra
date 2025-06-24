from .basic import Config
from .utils import Server, struct_path, struct_url
from ...errors.configs import ConfigSectionMissingError, ConfigParameterMissingError
from pathlib import Path

class RemoteConfig(Config):
    '''The class is defined for work with configurations of remote inference.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined for initialize RemoteConfig class object.'''
        # Initialize parent class
        super().__init__()
        # Define config attributes
        self.server:Server = None
        self.model:str = None
        # Define url attribute
        self.url:str = None

    ## ================================ Load Method ================================ ##
    def load(self,path:str|Path) -> None:
        '''The method is defined for load config file for local inference.
        Args:
            path: A string or Path instance indicate the path to the config file.
        '''
        # Load config file
        super()._load(path)        
        # Extra all remote parameters
        try:
            content:dict = self._content['remote']
        except KeyError:
            raise ConfigSectionMissingError('remote')
        # Read server config parameters
        ## Extra all server config parameters
        try:
            server = content['server']
        except KeyError:
            raise ConfigSectionMissingError('remote.server')
        ## Read server config parameters
        try:
            url = server['url']
        except KeyError:
            raise ConfigParameterMissingError('remote.server','url')
        else:
            url = struct_url(url)
        try:
            port = server['port']
        except KeyError:
            raise ConfigParameterMissingError('remote.server','port')
        try:
            endpoint = server['endpoint']
        except KeyError:
            raise ConfigParameterMissingError('remote.server','endpoint')
        else:
            endpoint = struct_path(endpoint)
        self.server:Server = Server(url,port,endpoint)
        # Read inference config parameter
        try:
            self.model = content['model']
        except KeyError:
            raise ConfigParameterMissingError('remote','model')
        # Make API url
        self.url = self.server.url
        self.url += ':' + str(self.server.port)
        self.url += '/' + self.server.endpoint
    
    ## =============================== Update Method =============================== ##
    def update(self,) -> None:
        '''The method is defined for update config parameters with inputs.'''
        pass