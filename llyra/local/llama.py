from . import config,prompt
from llama_cpp import Llama

## ========================== Initialize Function ========================== ##
def initialize(model:str,directory:str,gpu:bool) -> object:
    '''The function is defind for generate model object.
    Args:
        model: A string indicate the model file.
        directory: A string indicate the folder of model file.
        gpu: A bool indicate whether use GPU for acceleration.
    Returns:
        A object indicate Llama object of target model.
    '''
    # Make model file path
    path = config.path(model,directory)
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

