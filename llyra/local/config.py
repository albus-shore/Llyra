from pathlib import Path
import json

## ========================== Config Load Function ========================== ##
def load(path:str):
    '''The function is defined for load toolkit config file.
    Args:
        path: A string indicate the path to the config file.
    Returns:
        config:
            directory, model, gpu \n
            directory: A string indicate the folder of model file.\n
            model: A string indicate the name of model file.\n
            gpu: A boolean indicate whether using GPU for acceleration.\n
    '''
    # Load config file
    config_path:object = Path(path)
    try:
        config_json:str = config_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError('Error: Missing config file.')
    else:
        config_dictionary:dict = json.loads(config_json)
        # Read config parameter
        try:
            default_model:str = config_dictionary['model']
            directory:str = config_dictionary['directory']
            gpu:bool = config_dictionary['GPU']
        except IndexError:
            raise IndexError('Error: Missing necessary keys.')
        else:
            # Reture config parameter value
            return default_model,directory,gpu

## ========================== Name Function ========================== ##
def name(model:str) -> str:
    '''The function is defined for struct name of model file.
    Args:
        model: A string indicate the name of model file.
    Returns:
        name: A string indicate the name of model file without prefix.
    '''
    # Discriminate whether model file name with prefix
    if model.endswith('.gguf'):
        name = model[:-5]
    else:
        name = model
    # Return model file name value
    return name

## ========================= Folder Function ========================= ##
def folder(directory:str) -> str:
    '''The function is defined for struct directory of model file.
    Args:
        directory: A string indicate the folder of model file placed.
    Returns:
       folder: A string indicate the folder of model file placed with '/'.
    '''
    # Discriminate whether directory of model file end with '/'
    if directory.endswith('/'):
        folder = directory
    else:
        folder = directory + '/'
    # Return model file folder value
    return folder

## ========================== Path Function ========================== ##
def path(model:str,directory:str) -> str:
    '''The function is defined for generate model file path.
    Args:
        model: A string indicate the name of the model file.
        directory: A string indicate the folder of the model file placed.
    Returns:
        A string indicate the path of the model file.
    '''
    # Struct model file directory
    file_folder = folder(directory)
    # Struct model file name
    file_name = name(model)
    file_name += '.gguf'
    # Make model file path
    file_path = file_folder + file_name
    # Return model file path
    return file_path