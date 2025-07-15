from .iterations import Iteration
from dataclasses import dataclass, field

@dataclass
class Branch:
    '''The class is defined for managing branch records of inference.
    Args:
        id: A integer indicate the identity of current branch record.
        belonging: A integer indicate the belonging section of current branch record.
        iterations: A list of Iteration dataclass instances 
            indicate the inference history of current branch record.
    '''
    id: int
    belonging: int
    iterations: list[Iteration] = field(default_factory=list)