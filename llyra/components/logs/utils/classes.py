from dataclasses import dataclass,field
from typing import Literal
from time import time

@dataclass
class Section:
    '''The class is defined for making new chat history record.
    Args:
        id: A integrate indicate the identity of current chat log.
        model: A string indicate the name of model file.
        prompt: A string indicate the content of additional prompt.
        role: A dictionary indicate input and output role of
                iterative chat inference.
        temperature: A float indicate the model inference temperature.        
    '''
    id: int 
    type: Literal['call','chat']
    model: str
    prompt: str | None
    role: dict | None
    temperature: float
    iteration: list = field(default_factory=list)
    create_at: float = field(default_factory=time)