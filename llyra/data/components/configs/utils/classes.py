from dataclasses import dataclass
from pathlib import Path

## ========================== `LocalConfigData` Dataclass ========================== ##
@dataclass(frozen=True)
class LocalConfigData:
    '''This class is a dataclass contains information 
    for local inference configuration.
    Args:
        model: A `Path` instance indicates the location of local model file.
        format: A `str` indicates the format used for local chat inference.
        gpu: A `bool` indicates whether using gpu for local inference.
            Set `True` to use gpu, set `False` to use cpu.
        ram: A `bool` indicates whether keeping loading the model in local memory.
            Set `True` to keep, set `False` to release.
    '''
    model:Path
    format:str
    gpu:bool
    ram:bool 

## ========================= `RemoteConfigData` Dataclass ========================= ##
@dataclass(frozen=True)
class RemoteConfigData:
    '''This class is a dataclass contains information 
    for remote inference configuration.
    Args:
        model: A `str` indicates the model for remote inference.
        url: A `str` indicates the url to remote service.
    '''
    model:str
    url:str