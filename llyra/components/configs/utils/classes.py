from dataclasses import dataclass

## ============================== Dataclass `Model()` ============================== ##
@dataclass
class Model:
    '''
    The class is defined for managing parameters of model section in local section.
    Args:   
        name: A string indicate the name of local model for inference.
        directory: A string indicate the path of the directory placing the model file.
        suffix: A string indicate the suffix of model file format.
    '''
    name: str
    directory: str
    suffix: str

## ============================= Dataclass `Server()` ============================= ##
@dataclass
class Server:
    '''
    The class is defined for managing parameters of server section in remote section.
    Args:
        url: A string indicate the base url of remote inference server.
        port: A integrate indicate the service port of remote inference server.
        endpoint: A string indicate the endpoint before specific service interface.
    '''
    url: str
    port: int
    endpoint: str