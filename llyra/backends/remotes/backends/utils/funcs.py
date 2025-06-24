def convert_str2list(parameter:str|list) -> list:
    '''The function is defind for convert string parameter to list 
    for the needs of remote backend.
    Args:
        parameter: A string or list indicate the parameter for conversion.
    Returns:
        A list indicte the parameter in single object list.
    '''
    if type(parameter) == str:
        return [parameter]
    elif type(parameter) == list:
        return parameter