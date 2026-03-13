from .utils.classes import LocalConfigData,RemoteConfigData
from dataclasses import dataclass
from pathlib import Path

## ============================ `ConfigData` Dataclass ============================ ##
@dataclass(frozen=True)
class ConfigData:
    '''This class is a dataclass contains information 
    for general inference configuration.
    Args:
        model: A `str` indicates the name of model used for inference.
        strategy: A `Path` instance indicates the location of 
            inference strategy `toml` file.
        local: A `LocalConfigData` instance indicates 
            the local inference configuration.
        remote: A `RemoteConfigData` instance indicates 
            the remote inference configuration.
    '''
    model: str
    strategy: Path
    local: LocalConfigData
    remote: RemoteConfigData