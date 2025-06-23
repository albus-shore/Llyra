## ============================= Function `set_gpu()` ============================= ##
def set_gpu(gpu:bool) -> int:
    '''The function is defined for properly set whether using GPU for acceleration.
    Args:
        gpu: A boolean indicate whether using GPU for inference acceleration.
    Returns:
        layer: A integrate indicate number of layers offload to GPU.
    '''
    if gpu:
        layer = int(-1)
    else:
        layer = int(0)
    return layer