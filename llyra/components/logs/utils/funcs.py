from ...utils import Role
from ....utils import Iteration
from ....exceptions.components.logs import LogBaseFormatInvlidError
from json import loads, dumps, JSONDecodeError
from copy import deepcopy

## =========================== Function `convert2Role()` =========================== ##
def convert2Role(json:str|None) -> Role | None:
    '''The function is defined to 
    convert valid json string to a Role dataclass instance.
    Args:
        json: A json string indicate the data of Role dataclass instance.
            Or None indicate no data need to be converted.
    Returns:
        A Role dataclass instance indicate the data of json string.
        Or None indicate no data inputed.
    '''
    # Discriminate whether data inputed
    if json:
        # Convert json string to dict
        try:
            dictionary = loads(json)
        except JSONDecodeError:
            raise LogBaseFormatInvlidError()
        # Convert dict to dataclass
        try:
            role = Role(prompt=dictionary['prompt'],
                        input=dictionary['input'],
                        output=dictionary['output'])
        except KeyError:
            raise LogBaseFormatInvlidError()
    else:
        role = None
    # Return role data
    return role

## ====================== Function `convert2Iteration_list()` ====================== ##
def convert2Iteration_list(json_list:str) -> list[Iteration]:
    '''The function is defined to 
    convert valid json list string to a list of Iteration dataclass instances.
    Args:
        json_list: A json list string indicate 
            the data of list of Iteration dataclass instances.
    Returns:
        A list of Iteration dataclass instance indicate the data of json list string.
    '''
    # Convert json list string to list
    try:
        iteration_dicts = loads(json_list)
    except JSONDecodeError:
        raise LogBaseFormatInvlidError()
    # Convert dicts to dataclasses
    iterations = []
    for iteration_dict in iteration_dicts:
        try:
            iteration = Iteration(query=iteration_dict['query'],
                                  response=iteration_dict['response'])
        except KeyError:
            raise LogBaseFormatInvlidError()
        else:
            iterations.append(iteration)
    # Return iterations data
    return iterations

## =========================== Function `convert2json()` =========================== ##
def convert2json(role:Role) -> str:
    '''The function is defined to 
    convert a Role dataclass instance to valid json string.
    Args:
        role: A Role dataclass instance indicate the data of json string.
    Returns:
        A json string indicate the data of Role dataclass instance.
    '''
    # Deepcopy role
    internal_role = deepcopy(role)
    # Convert dataclass to dict
    role_dict = vars(internal_role)
    # Convert dict to json string
    json = dumps(role_dict,
                 ensure_ascii=False)
    # Return json string
    return json

## ======================== Function `convert2json_list()` ======================== ##
def convert2json_list(iterations:list[Iteration]) -> str:
    '''The function is defined to 
    convert a list of Iteration dataclass instances to valid json list string.
    Args:
        iterations: A list of Iteration dataclass instance 
            indicate the data of json list string.
    Returns:
        A json list string indicate the data of list of Iteration dataclass instances.
    '''
    # Deepcopy iterations
    internal_iterations = deepcopy(iterations)
    # Convert dataclasses to dicts
    iteration_dicts = []
    for iteration in internal_iterations:
        iteration_dict = vars(iteration)
        iteration_dicts.append(iteration_dict)
    # Convert dicts to json list string
    json_list = dumps(iteration_dicts,
                      ensure_ascii=False)
    # Return json list string
    return json_list