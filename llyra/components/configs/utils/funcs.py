## =========================== Function `struct_path()` =========================== ##
def struct_path(path:str) -> str:
    '''The method is defined for struct of multi-kind path/url.
    Args:
        path: A string indicate the local path to a directory 
            or endpoint to a service.
    Returns:
        structed_path: A string indicate the valid path string 
            which ends with '/'.
    '''
    # Discriminate whether path end with '/'
    if path.endswith('/'):
        structed_path = path
    else:
        structed_path = path + '/'
    # Return structed path
    return structed_path

## ========================== Function `struct_suffix()` ========================== ##
def struct_suffix(suffix:str) -> str:
    '''The method is defined for struct of local model file's suffix.
    Args:
        suffix: A string indicate the local model file's suffix.
    Returns:
        structed_suffix: A string indicate the valid suffix string 
            which starts with '.'
    '''
    # Discriminiate whether suffix strat with '.'
    if suffix.startswith('.'):
        structed_suffix = suffix
    else:
        structed_suffix = '.' + suffix
    # Return structed suffix
    return structed_suffix

## ======================== Function `struct_model_name()` ======================== ##
def struct_model_name(filename:str) -> str:
    '''The function is defined for struct name of local model file.
    Args:
        filename: A string indicate the name of local model file.
    Returns:
        name: A string indicate the name of model file without suffix.
    '''
    # Discriminate whether model file name with suffix
    if filename.endswith('.gguf'):
        name = filename.removesuffix('.gguf')
    else:
        name = filename
    # Return model file name value
    return name

## ============================ Function `struct_url()` ============================ ##
def struct_url(url:str) -> str:
    '''The function is defined for struct base url of remote server.
    Args:
        url: A string indicate the base url of remote server.
    Returns:
        structed_url: A string indicate the valid base url string.
    '''
    # Discriminate whether base url end with '/'
    if url.endswith('/'):
        structed_url = url.removesuffix('/')
    else:
        structed_url = url
    # Return structed url
    return structed_url