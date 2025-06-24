from dataclasses import dataclass, field
from typing import Literal
from time import time

from ...utils import Role

## ============================= Dataclass `Section()` ============================= ##
@dataclass
class Section:
    '''The class is defined for making chat history record.
    Args:
        id: A integrate indicate the identity of current chat log.
        model: A string indicate the name of model file.
        addition: A string indicate the content of additional prompt.
        role: A dataclass indicate input, output, and prompt role of
                iterative chat inference.
        temperature: A float indicate the model inference temperature.        
    '''
    id: int 
    type: Literal['call','chat']
    model: str
    addition: str | None
    role: Role | None
    temperature: float
    iteration: list = field(default_factory=list)
    create_at: float = field(default_factory=time)