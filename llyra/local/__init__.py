from .configs import ConfigLocal
from .strategys import StrategyLocal
from .prompts import PromptLocal
from .logs import LogLocal
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
class Local:
    '''The class is defined for fulfill local LLM call.'''

    ## ========================= Class Initialize Method ========================== ##
    def __init__(self,path:str=None) -> None:
        '''The method is defined for initialize Local class object.
        Args:
            path: A string indicate the path to config file.
        '''
        # Initialize necessary object attributes
        self.config = ConfigLocal()
        self.strategy = StrategyLocal()
        self.prompt = PromptLocal()
        self.log = LogLocal()
        # Import toolkit config
        self.config.load(path)
        # Import inference config
        self.strategy.load(self.config.strategy)
        # Initialize model Llama object
        self.model = Llama(model_path=self.config.path,
                           n_gpu_layers=gpu(self.config.gpu),
                           chat_format=self.config.format,
                           use_mlock=self.config.ram,
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
        self.strategy.update_call(input_role=input_role,output_role=output_role,
                           stop=stop,max_token=max_token,
                           temperature=temperature)
        # Get input content
        self.query = message
        # Make prompt
        prompt = self.prompt.call(self.strategy.call.role,self.query)
        # Fulfill model inference
        self.response = self.model.create_completion(prompt=prompt,
            stop=self.strategy.call.stop,
            max_tokens=self.strategy.call.tokens,
            temperature=self.strategy.call.temperature)['choices'][0]['text']
        # Update log
        self.log.call(model=self.config.model,
                      role=self.strategy.call.role,
                      input=self.query,output=self.response,
                      temperature=self.strategy.call.temperature)
        # Return model inference response
        return self.response

    def chat(self,message:str,keep:bool,
             *iteration:dict,addition:str=None,
             prompt_role:str=None,input_role:str=None,output_role:str=None,
             stop:str=None,max_token:int=None,
             temperature:float=None) -> str:
        '''The method is defined for fulfill iterative chat inference.
        Args:
            message: A string indicate the input content for chat inference.
            keep: A string indicate whether continue last chat iteration.
            iteration: A list of dictionaries contain 
                additional iteration history for the iterative chat inference.
            addition: A string indicate additional prompt 
                for the iterative chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            max_token: A integrate indicate 
                the max token number of model generation.
            temperature: A float indicate the model inference temperature.
        Returns:
            A string indicate the model response content of the chat inference.
        '''
        # Update inference strategy if necessary
        self.strategy.update_chat(addition,
                           prompt_role,input_role,output_role,
                           stop,max_token,
                           temperature)
        # Clear prompt iteration record if necessary
        self.prompt.iterate(None,None,keep)
        # Add additional prompt iteration record if necessary
        if iteration:
            self.prompt._iteration.extend(iteration)
        # Get input content
        self.query = message
        # Make prompt
        prompt = self.prompt.chat(self.strategy.chat.role,
                                  self.query,
                                  self.strategy.chat.prompt)
        # Fulfill model inference
        self.response = self.model.create_chat_completion(messages=prompt,
            stop=self.strategy.chat.stop,
            max_tokens=self.strategy.chat.tokens,
            temperature=self.strategy.chat.temperature
            )['choices'][0]['message']['content']
        # Update prompt iteration record
        self.prompt.iterate(self.strategy.chat.role['input'],self.query,True)
        self.prompt.iterate(self.strategy.chat.role['output'],self.response,True)
        # Update log
        self.log.chat(model=self.config.model,
                      prompt=self.strategy.chat.prompt,
                      role=self.strategy.chat.role,
                      input=self.query,output=self.response,
                      temperature=self.strategy.chat.temperature,
                      keep=keep)
        # Return model inference response
        return self.response