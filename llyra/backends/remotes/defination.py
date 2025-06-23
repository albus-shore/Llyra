from ...components import RemoteConfig, Strategy, Prompt, Log
from .backends import Ollama
from pathlib import Path

class Remote:
    '''The class is defined for fulfill remote LLM call.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,path:str|Path) -> None:
        '''The method is defined for initialize Remote class object.
        Args:
            path: A string or Path instance indicate the path to the config file.
        '''
        # Initialize component attributes
        self.config = RemoteConfig()
        self.strategy = Strategy()
        self.prompt = Prompt()
        self.log = Log()
        # Load remote config
        self.config.load(path)
        # Load inference strategy
        self.strategy.load(self.config.strategy)
        # Initialize backend attribute
        self.backend = Ollama(url=self.config.url,
                              model=self.config.model)
        # Define I/O attributes
        self.query: str
        self.response: str

    ## ============================= Inference Methods ============================= ##
    def call(self,message:str) -> str:
        '''The method is defined for fulfill single LLM call.
        Args:
            message: A string indicate the input content for model inference.
        Returns:
            A string indicate the output content from model inference.
        '''
        # Get input content
        self.query = message
        # Make prompt for inference
        prompt = self.prompt.call(self.query)
        # Execute model inference
        self.response = self.backend.call(prompt=prompt,
                                          stop=self.strategy.call.stop,
                                          temperature=self.strategy.call.temperature)
        # Make log record
        self.log.call(model=self.config.model,
                      input=self.query,output=self.response,
                      temperature=self.strategy.call.temperature)
        # Return model response
        return self.response
    
    def chat(self,message:str,keep:bool) -> str:
        '''The method is defined for fulfill iterative chat inference.
        Args:
            message: A string indicate the input content for chat inference.
            keep: A boolean indicate whether continue last chat iteration.
        Returns:
            response: A string indicate the output content from model inference.
        '''
        # Get input content
        self.query = message
        # Discriminate whether keep current section content
        self.prompt.iterate(None,None,None,keep)
        # Make prompt for inference
        prompt = self.prompt.chat(role=self.strategy.chat.role,
                                  content=self.query,
                                  addition=self.strategy.chat.addition)
        # Execute model inference
        self.response = self.backend.chat(prompt=prompt,
                                          stop=self.strategy.chat.stop,
                                          temperature=self.strategy.call.temperature)
        # Update prompt section content
        self.prompt.iterate(role=self.strategy.chat.role,
                            input=self.query,output=self.response,
                            keep=True)
        # Make log record
        self.log.chat(model=self.config.model,
                      addition=self.strategy.chat.addition,
                      role=self.strategy.chat.role,
                      input=self.query,output=self.response,
                      temperature=self.strategy.chat.temperature,
                      keep=keep)
        # Return model response
        return self.response