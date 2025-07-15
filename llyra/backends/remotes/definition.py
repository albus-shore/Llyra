from ...components import RemoteConfig, Strategy, Prompt, Log
from .backends import Ollama
from pathlib import Path

class Remote:
    '''The class is defined for fulfill remote LLM call.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,config:RemoteConfig,
                 strategy:Strategy,
                 prompt:Prompt,
                 log:Log) -> None:
        '''The method is defined for initialize Remote class object.
        Args:
        Args:
            config: A RemoteConfig class instance indicate the config status.
            strategy: A Strategy class instance indicate the strategy status.
            prompt: A Prompt class instance for inference prompt operation.
            log: A log class instance for log record operation.
        '''
        # Initialize component attributes
        self._config = config
        self._strategy = strategy
        self._prompt = prompt
        self._log = log
        # Define backend attribute
        self._backend = None
        # Define I/O attributes
        self.query: str
        self.response: str

    ## ================================ Load Method ================================ ##
    def load(self) -> None:
        '''The method is defined for load inference instance for inference.'''
        # Load backend attribute
        self._backend = Ollama(url=self._config.url,
                              model=self._config.model)

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
        prompt = self._prompt.call(self.query)
        # Execute model inference
        self.response = self._backend.call(prompt=prompt,
                                          stop=self._strategy.call.stop,
                                          temperature=self._strategy.call.temperature)
        # Make log record
        self._log.call(model=self._config.model,
                      input=self.query,output=self.response,
                      temperature=self._strategy.call.temperature)
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
        self._prompt.iterate(None,None,None,keep)
        # Make prompt for inference
        prompt = self._prompt.chat(role=self._strategy.chat.role,
                                  content=self.query,
                                  addition=self._strategy.chat.addition)
        # Execute model inference
        self.response = self._backend.chat(prompt=prompt,
                                          stop=self._strategy.chat.stop,
                                          temperature=self._strategy.call.temperature)
        # Update prompt section content
        self._prompt.iterate(role=self._strategy.chat.role,
                            input=self.query,output=self.response,
                            keep=True)
        # Make log record
        self._log.chat(model=self._config.model,
                      addition=self._strategy.chat.addition,
                      role=self._strategy.chat.role,
                      input=self.query,output=self.response,
                      temperature=self._strategy.chat.temperature,
                      keep=keep)
        # Return model response
        return self.response