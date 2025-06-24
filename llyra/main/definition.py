from ..backends import Local, Remote
from typing import Literal
from pathlib import Path

class Llyra:
    '''The class is defined for unified interface of inference and advance methods.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,mode:Literal['local','remote'],path:str|Path=None) -> None:
        '''The method is defined for initialize Llyra class object.
        Args:
            mode: A choice indicate the mode of Llyra.
            path: A string or Path instance indicate the path to the config file.
        '''
        # Initialize backend attribute
        if mode == 'local':
            self._backend = Local(path)
        elif mode == 'remote':
            self._backend = Remote(path)
    
    ## ============================= Inference Methods ============================= ##
    def call(self,input:str) -> str:
        '''The method is defined for fulfill single LLM call.
        Args:
            input: A string indicate the input content for model inference.
        Returns:
            output: A string indicate the output content from model inference.
        '''
        return self._backend.call(input)
    
    def chat(self,message:str,keep:bool) -> str:
        '''The method is defined for fulfill iterative chat inference.
        Args:
            message: A string indicate the input content for chat inference.
            keep: A boolean indicate whether continue last chat iteration.
        Returns:
            response: A string indicate the output content from model inference.
        '''
        return self._backend.chat(message,keep)
    
    ## ========================== Strategy Update Methods ========================== ##
    def update_call(self,stop:str|list=None,temperature:float=None) -> None:
        '''The method is defined for update strategy parameters 
        of single call inference.
        Args:
            stop: A string or a list of strings 
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        self._backend.strategy.update_call(stop,temperature)

    def update_chat(self,addition:str=None,
            prompt_role:str=None,input_role:str=None,output_role:str=None,
            stop:str|list=None,temperature:float=None) -> None:
        '''The method is defined for update strategy parameters 
        of iterative chat inference.
        Args:
            addition: A string indicate additional prompt for chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string or a list of strings
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        self._backend.strategy.update_chat(addition,
            prompt_role,input_role,output_role,
            stop,temperature)
        
    ## =========================== Config Update Method =========================== ##
    def update_config(self,format:str=None,gpu:bool=None,ram:bool=None) -> None:
        '''The method is defined for update config parameters 
        of local backend inference.
        Args:
            format: A sting indicate the format of chat inference's input.
            gpu: A boolean indicate whether using GPU for inference acceleration.
            ram: A boolean indicate whether keeping the model loaded in memory.
        '''
        try:
            self._backend.config.update(format,gpu,ram)
        except AttributeError:
            error = '`update_config()` only available with backend `local`.'
            raise AttributeError(error)
        
    ## ============================== Get Log Method ============================== ##
    def get_log(self,id:int) -> dict|list:
        '''The method is defined to read log records in reasonable way.
        Args:
            id: A integrate indicate the specific inference log.\n
                Start from 0. \n
                And read all records by set it minus.
        Returns:
            A dictionary indicate the specific log records.
            Or a list of each log record's dictionary. 
        '''
        return self._backend.log.get(id)   
