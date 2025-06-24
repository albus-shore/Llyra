from dataclasses import dataclass

@dataclass
class Role:
    '''This class is defined for managing role parameters.
    Args:
        prompt: A string indicate the role of additional prompt.
        input: A string indicate the role of input.
        output: A string indicate the role of output.
    '''
    prompt: str
    input: str
    output: str