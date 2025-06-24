from llama_cpp import Llama
from ...components import LocalConfig, Strategy, Prompt, Log
from .utils import set_gpu
from pathlib import Path

class Local:
    '''The class is defined for fulfill local LLM call.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,path:str|Path) -> None:
        '''The method is defined for initialize Local class object.
        Args:
            path: A string or Path instance indicate the path to the config file.
        '''
        # Initialize component attributes
        self.config = LocalConfig()
        self.strategy = Strategy()
        self.prompt = Prompt()
        self.log = Log()
        # Load local config
        self.config.load(path)
        # Load inference strategy
        self.strategy.load(self.config.strategy)
        # Initialize backend attribute
        self.backend = Llama(model_path=self.config.path,
                             n_gpu_layers=set_gpu(self.config.gpu),
                             chat_format=self.config.format,
                             use_mlock=self.config.ram,
                             n_ctx=0,
                             verbose=False)
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
        response = self.backend.create_completion(prompt=prompt,
            stop=self.strategy.call.stop,
            temperature=self.strategy.call.temperature)
        # Extra response content
        self.response = response['choices'][0]['text']
        # Make log record
        self.log.call(model=self.config.model.name,
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
        response = self.backend.create_chat_completion(messages=prompt,
            stop=self.strategy.chat.stop,
            temperature=self.strategy.chat.temperature)
        # Extra response content
        self.response = response['choices'][0]['message']['content']
        # Update prompt section content
        self.prompt.iterate(role=self.strategy.chat.role,
                            input=self.query,output=self.response,
                            keep=True)
        # Make log record
        self.log.chat(model=self.config.model.name,
                      addition=self.strategy.chat.addition,
                      role=self.strategy.chat.role,
                      input=self.query,output=self.response,
                      temperature=self.strategy.chat.temperature,
                      keep=keep)
        # Return model reponse
        return self.response