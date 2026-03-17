from ...data.components import StrategyData
from ...data.components.utils.roles import Role, LlamaCppRole
from ...data.components.startegys.untils.classes import CallStrategyData, \
    ChatStrategyData
from ...exceptions.components.strategys import StrategyOutOfRangeError, \
    StrategySectionMissingError, StrategyParameterMissingError, \
    StrategyCrashError, StrategyNoAvailableModeError
from tomllib import load as load_toml
from warnings import warn
from copy import deepcopy
from pathlib import Path


class Strategy:
    '''This class is a component for inference strategy manipulation.'''
    ## =============================== `load` Method =============================== ##
    def load(self,path:Path) -> StrategyData:
        '''The method will load strategy from designated `toml` file.
        Args:
            path: A `Path` instance indicates the path to 
                inference strategy `toml` file.
        '''
        # Load strategy content
        try:
            with path.open('rb') as obj:
                strategy:dict = load_toml(obj)
        except FileNotFoundError:
            raise FileNotFoundError('Strategy File Not Found.')
        # Read call attributes
        try:
            call_strategy:dict = strategy['call']
        except KeyError:
            # Make warning
            message = 'Missing `call` section in strategy file.\n'\
                '`call` inference not available.'
            warn(message=message,category=RuntimeWarning)
            # Make call strategy data False
            call_strategy_data = False
        else:
            # Read call stop
            try:
                call_stop:str|list = call_strategy['stop']
            except KeyError:
                raise StrategyParameterMissingError(section='call',
                                                    parameter='stop')
            # Read call temperature
            try:
                call_temperature:float = call_strategy['temperature']
            except KeyError:
                raise StrategyParameterMissingError(section='call',
                                                    parameter='temperature')
            # Build `CallStrategyData` dataclass
            call_strategy_data = CallStrategyData(stop=call_stop,
                                                  temperature=call_temperature)
        # Read chat attributes
        try:
            chat_strategy:dict = strategy['chat']
        except KeyError:
            # Make warning
            message = 'Missing `chat` section in strategy file.\n'\
                '`chat` inference not available.'
            warn(message=message,category=RuntimeWarning)
            # Make chat strategy data False
            chat_strategy_data = False
        else:
            # Read chat role attributes
            try:
                chat_role:dict = chat_strategy['role']
            except KeyError:
                raise StrategySectionMissingError('chat.role')
            else:
                # Read chat role prompt
                try:
                    chat_role_prompt = chat_role['prompt']
                except KeyError:
                    # Make warning
                    message = 'Missing `prompt` parameter in `chat.role` section '\
                        'in strategy file.\n'\
                        'Extra prompt not available(Crashing Exception).'
                    warn(message=message,category=RuntimeWarning)
                    # Make chat role prompt False
                    chat_role_prompt = False
                # Read chat role input
                try:
                    chat_role_input = chat_role['input']
                except KeyError:
                    raise StrategyParameterMissingError(section='chat.role',
                                                        parameter='input')
                # Read chat role output
                try:
                    chat_role_output = chat_role['output']
                except KeyError:
                    raise StrategyParameterMissingError(section='chat.role',
                                                        parameter='output')
                # Build `Role` dataclass
                chat_role_data = Role(prompt=chat_role_prompt,
                                      input=chat_role_input,
                                      output=chat_role_output)
            # Read chat prompt
            try:
                chat_prompt = chat_strategy['prompt']
            except KeyError:
                chat_prompt_str = False
            else:
                if chat_role_prompt != False:
                    chat_prompt_path = Path(chat_prompt)
                    try:
                        chat_prompt_str:str = chat_prompt_path.read_text('UTF-8')
                    except FileNotFoundError:
                        raise FileNotFoundError('Prompt File Not Found.')
                else:
                    raise StrategyCrashError()
            # Read chat stop
            try:
                chat_stop:str|list = chat_strategy['stop']
            except KeyError:
                raise StrategyParameterMissingError(section='chat',
                                                    parameter='stop')
            # Read chat temperature
            try:
                chat_temperature:float = chat_strategy['temperature']
            except KeyError:
                raise StrategyParameterMissingError(section='chat',
                                                    parameter='temperature')
            # Build `ChatStrategyData` dataclass
            chat_strategy_data = ChatStrategyData(role=chat_role_data,
                                                  prompt=chat_prompt_str,
                                                  stop=chat_stop,
                                                  temperature=chat_temperature)
        # Build & Return `StrategyData` dataclass
        if (call_strategy_data == False) and (chat_strategy_data == False):
            raise StrategyNoAvailableModeError()
        else:
            return StrategyData(call=call_strategy_data,chat=chat_strategy_data)

    ## ============================== Update Methods ============================== ##
    def call(self,strategy:StrategyData,
             stop:str|list=False,temperature:float=False) -> StrategyData:
        '''The method will build new `StrategyData` instance 
        with modified call inference strategy.
        Args:
            strategy: A `StrategyData` instance indicates 
                the original inference strategy.
            stop: A `str` or `list` indicates the token(s) stopping generation.
            temperature: A `float` indicates the temperature of model inference.
        '''
        # Verify strategy section initialization
        if strategy.call == False:
            raise StrategyOutOfRangeError('call')
        # Catch changing parameters
        if stop != False:
            stop_value = stop
        else:
            stop_value = strategy.call.stop
        if temperature != False:
            temperature_value = temperature
        else:
            temperature_value = strategy.call.temperature
        # Build & Reture new `StrategyData` dataclass
        return StrategyData(call=CallStrategyData(stop=stop_value,
                                                  temperature=temperature_value),
                            chat=deepcopy(strategy.chat))

    def chat(self,strategy:StrategyData,
             prompt:str=False,
             prompt_role:LlamaCppRole=False,
             input_role:LlamaCppRole=False,output_role:LlamaCppRole=False,
             stop:str|list=False,temperature:float=False) -> StrategyData:
        '''The method will build new `StrategyData` instance 
        with modified chat inference strategy.
        Args:
            strategy: A `StrategyData` instance indicates 
                the original inference strategy.
            prompt: A `str` indicates the outside prompt for chat inference.
            prompt_role: A given `str` indicates the role of outside prompt.
            input_role: A given `str` indicates the role of input.
            output_role: A given `str` indicate the role of output 
                as known as the model response.
            stop: A `str` or `list` indicates the token(s) stopping generation.
            temperature: A `float` indicates the temperature of model inference.
        '''
        # Verify strategy section initialization
        if strategy.chat == False:
            raise StrategyOutOfRangeError('chat')
        # Catch changing parameters
        if prompt != False:
            prompt_value = prompt
        else:
            prompt_value = strategy.chat.prompt
        if prompt_role != False:
            role_prompt = prompt_role
        else:
            role_prompt = strategy.chat.role.prompt
        if input_role != False:
            role_input = input_role
        else:
            role_input = strategy.chat.role.input
        if output_role != False:
            role_output = output_role
        else:
            role_output = strategy.chat.role.output
        if stop != False:
            stop_value = stop
        else:
            stop_value = strategy.chat.stop
        if temperature != False:
            temperature_value = temperature
        else:
            temperature_value = strategy.chat.temperature
        # Check compliance
        if prompt_value and (role_prompt == False):
            raise StrategyCrashError()
        # Build & Return new `StrategyData` dataclass
        return StrategyData(call=deepcopy(strategy.call),
                            chat=ChatStrategyData(role=Role(prompt=role_prompt,
                                                            input=role_input,
                                                            output=role_output),
                                                  prompt=prompt_value,
                                                  stop=stop_value,
                                                  temperature=temperature_value))