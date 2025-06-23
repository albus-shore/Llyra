from .utils import Call, Chat
from ..utils import Role
from ...errors.strategys import StrategySectionMissingError, StrategyParameterMissingError
from warnings import warn
from pathlib import Path
import tomllib

class Strategy:
    '''The class is defined to define universal attributes and methods,
    for working with inference strategies.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined for initalizeing Strategy class object.'''
        # Define necessary object attributes
        self.call:Call = None
        self.chat:Chat = None

    ## ================================ Load Method ================================ ##
    def load(self,path:Path) -> None:
        '''The method is defined for loading strategy content from file.
        Args:
            path: A Path instance indicate the path to the strategy file.
        '''
        # Load strategy file
        try:
            with path.open('rb') as obj:
                content = tomllib.load(obj)
        except FileNotFoundError:
            raise FileNotFoundError('Strategy file not found in provided path.')
        # Read call strategy parameters
        ## Extra all call strategy parameters
        try:
            call = content['call']
        except KeyError:
            raise StrategySectionMissingError('call')
        ## Read call strategy parameters
        try:
            stop = call['stop']
        except KeyError:
            message = 'Missing `stop` parameter of `call` section '
            message += "in `strategy.toml` , auto-fallback to `[]`."
            warn(message,RuntimeWarning)
            stop = []
        try:
            temperature = call['temperature']
        except KeyError:
            message = 'Missing `temperature` parameter of `call` section '
            message += 'in `strategy.toml` , auto-fallback to `0`.'
            warn(message,RuntimeWarning)
            temperature = 0
        self.call:Call = Call(stop,temperature)
        # Read chat strategy parameters
        ## Extra all chat strategy parameters
        try:
            chat = content['chat']
        except KeyError:
            raise StrategySectionMissingError('chat')
        ## Read additonal prompt
        try:
            addition_path = chat['prompt']
        except KeyError:
            addition = None
        else:
            addition_obj = Path(addition_path)
            try:
                addition = addition_obj.read_text(encoding='utf-8')
            except FileNotFoundError:
                raise FileNotFoundError('Prompt file not found in provided path.')
        ## Read chat role parameters
        ### Etra all chat role parameters
        try:
            role_content = chat['role']
        except KeyError:
            raise StrategySectionMissingError('chat.role')
        ### Read chat role parameters
        try:
            prompt = role_content['prompt']
        except KeyError:
            if addition:
                raise StrategyParameterMissingError('chat.role','prompt')
            else:
                prompt = None
        try:
            input = role_content['input']
        except KeyError:
            raise StrategyParameterMissingError('chat.role','input')
        try:
            output = role_content['output']
        except KeyError:
            raise StrategyParameterMissingError('chat.role','output')
        role = Role(prompt,input,output)
        ## Read other chat strategy parameters
        try:
            stop = chat['stop']
        except KeyError:
            message = 'Missing `stop` parameter of `chat` section '
            message += "in `strategy.toml` , auto-fallback to `[]`."
            warn(message,RuntimeWarning)
            stop = []
        try:
            temperature = chat['temperature']
        except KeyError:
            message = 'Missing `temperature` parameter of `chat` section '
            message += "in `strategy.toml` , auto-fallback to `0`."
            warn(message,RuntimeWarning)
            temperature = 0
        self.chat:Chat = Chat(role,addition,stop,temperature)

    ## ============================== Update Methods ============================== ##
    def update_call(self,stop:str|list,temperature:float) -> None:
        '''The method is defined for update inference strategy for call.
        Args:
            stop: A string or a list of strings 
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        if stop != None:
            self.call.stop = stop
        if temperature != None:
            self.call.temperature = temperature

    def update_chat(self,addition:str,
                    prompt_role:str,input_role:str,output_role:str,
                    stop:str|list,temperature:float) -> None:
        '''The method is defined for update inference strategy for chat.
        Args:
            addition: A string indicate additional prompt for chat inference.
            prompt_role: A string indicate the role of additional prompt.
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string or a list of strings
                indicate where the model should stop generation.
            temperature: A float indicate the model inference temperature.
        '''
        if addition != None:
            self.chat.addition = addition
        if prompt_role != None:
            if (not prompt_role) and (self.chat.addition):
                error = "`prompt` parameter of `chat.role` setting can't be empty "
                error += "when `addition` parameter of `chat` setting isn't empty. "
                raise ValueError(error)
            else:
                self.chat.role.prompt = prompt_role
        if input_role != None:
            self.chat.role.input = input_role
        if output_role != None:
            self.chat.role.output = output_role
        if stop != None:
            self.chat.stop = stop
        if temperature != None:
            self.chat.temperature = temperature
                    