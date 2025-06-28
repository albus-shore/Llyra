from .classes import Iteration
from copy import deepcopy
import json

## ====================== Function `convert_dataclass2json()` ====================== ##
def convert_dataclass2json(dataclass:object) -> str:
    '''The function is defined for convert internal dataclass to json str.
    Args:
        dataclass: A dataclass instance for conversion.
    Returns:
        A json string indicate the data in converted dataclass.
    '''
    # Copy dataclass
    internal_dataclass = deepcopy(dataclass)
    # Convert dataclass to dictionary
    dictionary_data = vars(internal_dataclass)
    # Convert dictionary to json string
    string_data = json.dumps(dictionary_data)
    # Return coverted data
    return string_data

## ==================== Function `convert_dataclasses2jsonlist` ==================== ##
def convert_dataclasses2jsonlist(dataclasses:list) -> str:
    '''The function is defined for covert a list of dataclasses to a json list str.
    Args:
        dataclasses: A list of dataclass instances for conversion.
    Returns:
        A json list string indicate the data in converted dataclasses.
    '''
    # Copy dataclasses
    internal_dataclasses = deepcopy(dataclasses)
    # Prepare json list
    json_list = []
    # Convert dataclass to dictionary
    for dataclass in internal_dataclasses:
        dictionary_data = vars(dataclass)
        json_list.append(dictionary_data)
    # Convert list to json list string
    json_list_str = json.dumps(json_list)
    # Return json list string
    return json_list_str

## ==================== Function `convert_jsonlist2dataclasses` ==================== ##
def convert_jsonlist2dataclasses(jsonlist:str) -> list[Iteration]:
    '''The function is defined for convert a json list str to a list of dataclasses.
    Specificial convert to a list of Iteration class instances.
    Args:
        jsonlist: A json list string indicate for conversion.
    Returns:
        A list of dataclass instances indicate the data in converted json list str.
    '''
    # Convert json list string to dict list
    dict_list = json.loads(jsonlist)
    # Prepare dataclasses
    dataclasses = []
    # Convert dictionary to dataclass
    for dictionary in dict_list:
        iteration = Iteration(query=dictionary['query'],
                              response=dictionary['response'])
        dataclasses.append(iteration)
    # Return dataclasses
    return dataclasses