from ..base import Strategy

### =============================== Expose Class =============================== ###
class StrategyRemote(Strategy):
    '''The class is defind for work with inference strategies 
        of remote inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize StrategyRemote class object.'''
        # Initialize parent class
        super().__init__()
        # Define single call strategy
        self.call.system = None
        self.call.stop = None
        self.call.temperature = None
        # Define iterative chat strategy
        self.chat.stop = None
        self.chat.temperature = None

    ## ============================= Load Method ============================= ##   
    def load(self,path:str) -> None:
        '''The method is defined for load strategy file for remote inference.
        Args:
            path: A string indicate the path to the strategy file.
        '''
        # Define strategy loading method
        def call(strategy:dict):
            self.call.system = strategy.get('system',None)
            self.call.stop = strategy.get('stop',None)
            self.call.temperature = strategy.get('temperature',0)
        def chat(strategy:dict):
            self.chat.stop = strategy.get('stop',None)
            self.chat.temperature = strategy.get('temperature',0)
        # Load strategy
        super()._load(path,call,chat)    

    ## =========================== Update Methods =========================== ##
    def update_call(self,system:str,stop:str,temperature:float) -> None:
        '''The method is defined for update inference strategy for call.
        Args:
            system: A string indicate system prompt for model inference.
            stop: A string indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        if system != None:
            self.call.system = system
        if stop != None:
            self.call.stop = stop
        if temperature != None:
            self.call.temperature = temperature

    def update_chat(self,prompt:str,
                    prompt_role:str,input_role:str,output_role:str,
                    stop:str,temperature:float) -> None:
        '''The method is defined for update inference strategy for chat.
        Args:
            prompt: A string indicate additional prompt for chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        # Update strategy parameters
        self.chat.update(prompt,
                         prompt_role,input_role,output_role)
        if stop != None:
            self.chat.stop = stop
        if temperature != None:
            self.chat.temperature = temperature