from ...data.components import ConfigData
from ...data.components.configs.utils.classes import LocalConfigData, RemoteConfigData
from ...exceptions.components.configs import ConfigSectionMissingError, \
    ConfigParameterMissingError, ConfigUnsupportedInferenceModeError
from .utils.funcs import struct_model_name, struct_path, struct_suffix, struct_url
from tomllib import load as load_toml
from warnings import warn
from pathlib import Path
from typing import Literal


class Config:
    '''This class is a component for inference configuration manipulation.'''
    ## ================================ Class Args ================================ ##
    path:Path = Path('configs/config.toml')

    ## =============================== `load` Method =============================== ##
    def load(self,mode:Literal['Local','Remote']) -> ConfigData:
        '''The method will load configuration from designated `toml` file.
        Args:
            mode: A given `str` indicates inference backend.
        '''
        # Load config content
        try:
            with self.path.open('rb') as obj:
                configuration:dict = load_toml(obj)
        except FileNotFoundError:
            raise FileNotFoundError('Configuration File Not Found.')
        # Read global attributes
        try:
            global_config:dict = configuration['global']
        except KeyError:
            raise ConfigSectionMissingError('global')
        else:
            try:
                strategy_path = global_config['strategy']
            except KeyError:
                raise ConfigParameterMissingError(section='global',
                                                  parameter='strategy')
            else:
                strategy = Path(strategy_path)
        # Read local or remote attributes
        if mode == 'Local':
            # Read local attributes
            try:
                local_config = configuration['local']
            except KeyError:
                raise ConfigSectionMissingError('local')
            else:
                # Read local model attributes
                try:
                    local_model:dict = local_config['model']
                except KeyError:
                    raise ConfigSectionMissingError('local.model')
                else:
                    # Read local model name
                    try:
                        local_model_name:str = local_model['name']
                    except KeyError:
                        raise ConfigParameterMissingError(section='local.model',
                                                        parameter='name')
                    else:
                        local_model_name = struct_model_name(local_model_name)
                    # Read local model directory
                    try:
                        local_model_directory:str = local_model['directory']
                    except KeyError:
                        raise ConfigParameterMissingError(section='local.model',
                                                        parameter='directory')
                    else:
                        local_model_directory = struct_path(local_model_directory)
                    # Read local model suffix
                    try:
                        local_model_suffix:str = local_model['suffix']
                    except KeyError:
                        raise ConfigParameterMissingError(section='local.model',
                                                        parameter='suffix')
                    else:
                        local_model_suffix = struct_suffix(local_model_suffix)
                    # Build local model path
                    local_model_path = local_model_directory + local_model_name + \
                        local_model_suffix
                    local_model_path = Path(local_model_path)
                # Read local inference environmrnt attributes
                try:
                    local_format = local_config['format']
                except KeyError:
                    message = 'Missing `format` parameter in `local` section, '\
                        'fallback to `None`.'
                    warn(message=message,category=RuntimeWarning)
                    local_format = None
                try:
                    local_gpu = local_config['gpu']
                except KeyError:
                    message = 'Missing `gpu` parameter in `local` section, '\
                        'fallback to `False`.'
                    warn(message=message,category=RuntimeWarning)
                    local_gpu = False
                try:
                    local_ram = local_config['ram']
                except KeyError:
                    message = 'Missing `ram` parameter in `local` section, '\
                        'fallback to `False`.'
                    warn(message=message,category=RuntimeWarning)
                    local_ram = False
                # Build `LocalConfigData` dataclass
                local_config_data = LocalConfigData(model=local_model_path,
                                                    format=local_format,
                                                    gpu=local_gpu,
                                                    ram=local_ram)
                # Build & Return `ConfigData` dataclass
                return ConfigData(model=local_model_name,
                                  strategy=strategy,
                                  local=local_config_data,
                                  remote=False)
        elif mode == 'Remote':
            # Read remote attributes
            try:
                remote_config = configuration['remote']
            except KeyError:
                raise ConfigSectionMissingError('remote')
            else:
                # Read remote model
                try:
                    remote_model = remote_config['model']
                except KeyError:
                    raise ConfigParameterMissingError(section='remote',
                                                    parameter='model')
                # Read remote service attributes
                try:
                    remote_service:dict = remote_config['service']
                except KeyError:
                    raise ConfigSectionMissingError('remote.service')
                else:
                    # Read remote service url
                    try:
                        remote_service_url = remote_service['url']
                    except KeyError:
                        raise ConfigParameterMissingError(section='remote.service',
                                                        parameter='url')
                    else:
                        remote_service_url = struct_url(remote_service_url)
                    # Read remote service port
                    try:
                        remote_service_port = remote_service['port']
                    except KeyError:
                        raise ConfigParameterMissingError(section='remote.service',
                                                        parameter='port')
                    else:
                        remote_service_port = str(remote_service_port)
                    # Read remote service endpoint
                    try:
                        remote_service_endpoint = remote_service['endpoint']
                    except KeyError:
                        raise ConfigParameterMissingError(section='remote.service',
                                                        parameter='endpoint')
                    else:
                        remote_service_endpoint = struct_path(remote_service_endpoint)
                    # Build remote service path
                    remote_service_path = remote_service_url + ':' + \
                        remote_service_port + '/' + remote_service_endpoint
                # Build `RemoteConfigData` dataclass
                remote_config_data = RemoteConfigData(model=remote_model,
                                                    url=remote_service_path)
                # Build & Return `ConfigData` dataclass
                return ConfigData(model=remote_model,
                                  strategy=strategy,
                                  local=False,
                                  remote=remote_config_data)
        else:
            # Catch unsupported inference mode
            raise ConfigUnsupportedInferenceModeError(mode)
        
    ## =============================== `set` Method =============================== ##
    def set(self,path:Path|str) -> None:
        '''The method will set new `Path` instance to self attribute `path`.
        Args:
            path: A `Path` instance or `str` indicates the new path to 
                inference config `toml` file.
        '''
        # Set new path
        if isinstance(path,Path):
            self.path = path
        else:
            self.path = Path(path)