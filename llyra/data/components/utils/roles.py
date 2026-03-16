from dataclasses import dataclass
from typing import Literal

## ============================= Assistant string type ============================= ##
LlamaCppRole = Literal['system','user','assistant']

## =============================== `Role` dataclass =============================== ##
@dataclass(frozen=True)
class Role:
    '''This class is a dataclass contains information 
    indicating the role strategy for chat inference.
    Args:
        prompt: A given `str` indicates the role of outside prompt.
        input: A given `str` indicates the role of input.
        output: A given `str` indicate the role of output 
            as known as the model response.
    '''
    prompt:LlamaCppRole
    input:LlamaCppRole
    output:LlamaCppRole