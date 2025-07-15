from dataclasses import dataclass

@dataclass
class Iteration:
    '''The class is defined for managing iteration records of inference.
    Args:
        query: A string indicate input content for model inference.
        response: A string indicate response of model inference.    
    '''
    query: str
    response: str