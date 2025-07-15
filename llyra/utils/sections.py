from ..components.utils import Role
from dataclasses import dataclass, field
from typing import Literal
from time import time

@ dataclass
class Section:
    '''The class is defined for managing section records of inference.
    Args:
        id: A integer indicate the identity of current section record.
        type: A string with fixed choices indicate the inference mode 
            of current section record.
        model: A string indicate the name of inference model.
        addition: A string indicate the content of additional prompt.
        role: A Role dataclass instance indicate input, output, and prompt role of
            iterative chat inference.
        temperature: A float indicate the model inference temperature.
    '''
    id: int
    type: Literal['call','chat']
    model: str
    addition: str | None
    role: Role | None
    temperature: float
    create_at: float = field(default_factory=time)