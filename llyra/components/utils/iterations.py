from dataclasses import dataclass

@dataclass
class Iteration:
    '''The class is defined for managing iteration record in branch record.
    Args:
        query: A string indicate input content for model inference.
        response: A string indicate response of model inference.
    '''
    query: str
    response: str