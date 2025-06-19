## ========================== Function `make_new_iteration()` ========================== ##
def make_new_iteration(input:str,output:str) -> dict:
    '''The function is defined for make valid record of each iteration.
    Agrs:
        input: A string indicate input content for model inference. 
        output: A string indicate response of model inference.
    Returns:
        A dictionary indicate the record of the iteration.
    '''
    return {'query': input, 'response': output}