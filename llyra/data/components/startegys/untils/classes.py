from ...utils.roles import Role
from dataclasses import dataclass

## ========================= `CallStrategyData` Dataclass ========================= ##
@dataclass(frozen=True)
class CallStrategyData:
    '''This class is a dataclass contains information 
    for call inference strategy control.
    Args:
        stop: A `str` or `list` indicates the token(s) stopping generation.
        temperature: A `float` indicates the temperature of model inference.
    '''
    stop:str|list
    temperature:float

## ========================= `ChatStrategyData` Dataclass ========================= ##
@dataclass(frozen=True)
class ChatStrategyData:
    '''This class is a dataclass contains information 
    for chat inference strategy control.
    Args:
        role: A `Role` instance indicates the role strategy for chat inference.
        prompt: A `str` indicates the outside prompt for chat inference, 
            which will be added to prompt at the beginning.
        stop: A `str` or `list` indicates the token(s) stopping generation.
        temperature: A `float` indicates the temperature of model inference.
    '''
    role:Role
    prompt:str
    stop:str|list
    temperature:float