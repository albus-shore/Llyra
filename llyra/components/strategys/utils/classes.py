from ...utils import Role
from dataclasses import dataclass

## ============================== Dataclass `Call()` ============================== ##
@dataclass
class Call:
    '''The class is defined for work with strategies with 
    universal single call inference.
    Args:
        stop: A string indicate where the model should stop generation.
        temperature: A float indicate the model inference temperature.
    '''
    stop: str|list
    temperature: float

## ============================== Dataclass `Chat()` ============================== ## 
@dataclass
class Chat:
    '''The class is defined for work with strategies with
    universal iterative chat inference.
    Args:
        role: A dataclass indicate input, output, and prompt role of 
            iterative chat inference.
        addition: A string indicate additional prompt for chat inference.
        stop: A string indicate where the model should stop generation.
        temperature: A float indicate the model inference temperature.
    '''
    role: Role
    addition: str
    stop: str|list
    temperature: float    