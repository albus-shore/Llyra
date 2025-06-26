## ================================= Config Error ================================= ##
class ConfigError(Exception):
    '''The class is defined as the base of all custom errors of config process.'''
    pass

## ============================= Section Missing Error ============================= ##
class ConfigSectionMissingError(ConfigError):
    '''The class is defined for indicate error 
    when config file missing necessary sections.'''
    def __init__(self,section:str):
        '''
        Args:
            section: A string indicate the missing section in config file.
        '''
        indication = f'Missing `{section}` section in `config.toml`.'
        super().__init__(indication)

## ============================ Parameter Missing Error ============================ ##
class ConfigParameterMissingError(ConfigError):
    '''The class is defined for indicate error 
    when config file missing necessary parameters.'''
    def __init__(self,section:str,parameter:str):
        '''
        Args:
            section: A string indicate the belonging section of the missing parameter.
            parameter: A string indicate the missing parameter in config file.
        '''
        indication = f'Missing `{parameter}` parameter of `{section}` section '
        indication += 'in `config.toml`.'
        super().__init__(indication)