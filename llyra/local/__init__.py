from .configs import Config
from .strategys import Strategy
from .prompts import Prompt
from .logs import Log
from llama_cpp import Llama

### =============================== Inside Functions =============================== ###
## =============================== GPU Set Function =============================== ##
def gpu(gpu:bool) -> int:
    '''The function is defined for properly set whether using GPU for acceleration.
    Args:
        gpu: A boolean indicate whether using GPU for inference acceleration.
    Returns:
        layer: A integrate indicate number of layers offload to GPU.
    '''
    if gpu:
        layer = int(-1)
    else:
        layer = int(0)
    return layer

### ================================= Expose Class ================================= ###
class Model:
    '''The class is defined for fulfill local LLM call.'''

    ## ========================= Class Initialize Method ========================== ##
    def __init__(self,path:str=None) -> object:
        '''The method is defined for initialize model object.
        Args:
            path: A string indicate the path to config file.
        Returns:
            A target LLM loaded Model object.
        '''
        # Initialize necessary object attributes
        self.config = Config()
        self.strategy = Strategy()
        self.prompt = Prompt()
        self.log = Log()
        # Import toolkit config
        self.config.load(path)
        # Import inference config
        self.strategy.load(self.config.strategy)
        self.prompt.config(self.config.indicate)
        # Initialize model Llama object
        self.model = Llama(model_path=self.config.path,
                           n_gpu_layers=gpu(self.config.gpu),
                           use_mlock=self.config.ram or False,
                           n_ctx=0,
                           verbose=False)
        # Initialize current inference attributea
        self.query:str
        self.response:str

    ## ========================== Call Method ========================== ##
    def call(self,message:str,
             input_role:str=None,output_role:str=None,
             stop:str=None,max_token:int=None,
             temperature:int=None) -> str:
        '''The method is defined for fulfill single LLM call.
        Args:
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model reponse content.
        '''
        # Update inference strategy if necessary
        self.strategy.call(input_role=input_role,output_role=output_role,
                           stop=stop,max_token=max_token,
                           temperature=temperature)
        # Set prompt object necessary attribute
        self.prompt.set(self.strategy.call_role)
        # Get input content
        self.query = message
        # Make prompt
        prompt = self.prompt.call(self.query)
        # Fulfill model inference
        self.response = self.model.create_completion(prompt=prompt,
            stop=self.strategy.call_stop,
            max_tokens=self.strategy.call_tokens,
            temperature=self.strategy.call_temperature)['choices'][0]['text']
        # Update log
        self.log.call(model=self.config.model,
                      role=self.strategy.call_role,
                      input=self.query,output=self.response,
                      temperature=self.strategy.call_temperature,
                      strategy=self.config.strategy)
        # Return model inference response
        return self.response
