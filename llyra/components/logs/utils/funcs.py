from .classes import Section

## ======================== Function `make_new_iteration()` ======================== ##
def make_new_iteration(input:str,output:str) -> dict:
    '''The function is defined for make valid record of each iteration.
    Agrs:
        input: A string indicate input content for model inference. 
        output: A string indicate response of model inference.
    Returns:
        A dictionary indicate the record of the iteration.
    '''
    return {'query': input, 'response': output}

## ======================= Function `convert2readable_log()` ======================= ##
def convert2readable_log(section:Section) -> dict:
    '''The function is defined for covert internal log format to readable format.
    Args:
        section: A dataclass indicate log record of inference.
    Returns:
        readable_record: A dictionary indicate the readable log record of inference.
    '''
    # Covert record in first layer
    readable_record = vars(section)
    # Discriminate whether necessary to convert record in second layer
    if section.role:
        readable_record['role'] = vars(section.role)
    # Return readable record
    return readable_record