from . import prompt
from llama_cpp import Llama

## ========================== Initialize Function ========================== ##
def initialize(path:str,gpu:bool) -> object:
    '''The function is defind for generate model object.
    Args:
        path: A string indicate the path to the model file.
        gpu: A bool indicate whether use GPU for acceleration.
    Returns:
        A object indicate Llama object of target model.
    '''
    # Make number of layers offload to GPU
    if gpu:
        layer:int = -1
    else:
        layer:int = 0
    # Initialize model Llama object
    try:
        LLM = Llama(model_path=path,
                    n_gpu_layers=layer)
    except ValueError:
        raise FileNotFoundError('Error: Model file not found.')
    else:
        # Return mdel Llama object
        return LLM

