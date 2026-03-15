from ...exceptions import LlyraError

## ================================== Basic Error ================================== ##
class ConfigError(LlyraError):
    '''This exception is the base of all config related errors.'''
    pass

## ============================ `SectionMissing` Error ============================ ##
class ConfigSectionMissingError(ConfigError):
    '''The exception indicates the missing of the showing key section 
    in the config file.'''
    def __init__(self,section:str):
        '''
        Args:
            section: A `str` indicates the name of the missing section.
        '''
        indication = f'Missing `{section}` section in config file.'
        super().__init__(indication)

## =========================== `ParameterMissing` Error =========================== ##
class ConfigParameterMissingError(ConfigError):
    '''The exception indicates the missing of the showing key parameter
    in the showing section in the config file.'''
    def __init__(self,section:str,parameter:str):
        '''
        Args:
            section: A `str` indicates the section of the missing parameter.
            parameter: A `str` indicates the name of the missing parameter.
        '''
        indication = f'Missing `{parameter}` parameter in `{section}` section '\
            'in config file.'
        super().__init__(indication)

## ======================= `UnsupportedInferenceMode` Error ======================= ##
class ConfigUnsupportedInferenceModeError(ConfigError):
    '''The exception indicates the unsupport of the designated inference mode.'''
    def __init__(self,mode:str):
        '''
        Args:
            mode: A `str` indicates the unsupported inference mode.
        '''
        indication = f'Inference mode `{mode}` is not supported.\n'\
            'Choose `Local` or `Remote` instead.'
        super().__init__(indication)