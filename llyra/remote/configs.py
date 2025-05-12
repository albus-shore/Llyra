from warnings import warn
from ..base import Config

### ============================= Inside Functions ============================= ###
## =============== Necessary Parameters Check Function =============== ##
def check_necessary(model:str,strategy:str) -> None:
    '''The function is defined for check necessary config parameters.
    Args:
        model: A string indicate the model for inference.
        strategy: A string indicate the path to the inference strategy file.
    '''
    if not model:
        warning = 'Warning: Missing instructed model for inference.\n'
        warning += '\t\t All inference unavailiable without manual updating.'
        warn(warning,UserWarning)
    if not strategy:
        warning = 'Warning: Missing inference file.\n'
        warning += '\t\t Chat inference unavailiable without manual updating.'
        warn(warning,UserWarning)

### =============================== Expose Class =============================== ###
class ConfigRemote(Config):
    '''The class is defined for work with configurations of remote inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize ConfigRemote class object.'''
        # Initialize parent class
        super().__init__()
        # Define config attributes
        self.url:str = None
        self.endpoint:str = None
        self.model:str = None
        self.strategy: str = None
        self.stream: bool = None

    ## ============================= Load Method ============================= ##
    def load(self,path:str=None) -> None:
        '''The method is defined for load config file for remote inference.
        Args:
            path: A string indicate the path to the config file.
        '''
        # Load config file
        super()._load(path=path)
        # Read config parameter
        self.url = self._config.get('url',None)
        self.endpoint = self._config.get('endpoint',None)
        self.model = self._config.get('model',None)
        self.strategy = self._config.get('strategy',None)
        self.stream = self._config.get('stream',False)
        # Critical parameters check
        if not self.url:
            error = 'Error: Missing base URL parameter.'
            raise IndexError(error)
        if not self.endpoint:
            error = 'Error: Missing service endpoint parameter.'
            raise IndexError(error)
        # Necessary parameters check
        check_necessary(self.model,self.strategy)
        # Fix possible invalid attribute
        self.url = super().path(self.url)
        self.endpoint = super().path(self.endpoint)

    ## ============================ Update Method ============================ ##
    def update(self,
               url:str,
               endpoint:str,
               model:str,
               strategy:str,
               stream:bool) -> None:
        '''The method is defined for update config parameters with inputs.
        Args:
            url: A string indicate the base URL of service.
            endpoint: A string indicate the endpoint of service.
            model: A string indicate the model for inference.
            strategy: A string indicate the path to the inference strategy file.
            stream: A boolean indicate streaming reponse of inference.
        '''
        # Update parameter according to the input
        ## Update key parameters
        if url:
            self.url = super().path(url)
        if endpoint:
            self.endpoint = super().path(endpoint)
        ## Update normal parameter
        if model != None:
            self.model = model
        if strategy != None:
            self.strategy = strategy
        if stream != None:
            self.stream = stream
        # Necessary parameters check 
        check_necessary(self.model,self.strategy)

    ## ============================ Write Method ============================ ##
    def write(self) -> None:
        '''The method is defined for writing current config into file.'''
        # Prepare content
        content = {
            'url': self.url,
            'endpoint': self.endpoint,
            'model': self.model,
            'strategy': self.strategy,
            'stream': self.stream
            }
        super()._write(content=content)    