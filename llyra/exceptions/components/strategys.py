from ...exceptions import LlyraError
from typing import Literal

## ================================== Basic Error ================================== ##
class StrategyError(LlyraError):
    '''This exception is the base of all strategy related errors.'''
    pass

## ============================ `SectionMissing` Error ============================ ##
class StrategySectionMissingError(StrategyError):
    '''This exception indicates the missing of the showing key section 
    in the strategy file.'''
    def __init__(self,section:str):
        '''
        Args:
            section: A `str` indicates the name of the missing section.
        '''
        indication = f'Missing `{section}` section in strategy file.'
        super().__init__(indication)

## =========================== `ParameterMissing` Error =========================== ##
class StrategyParameterMissingError(StrategyError):
    '''This exception indicates the missing of the showing key parameter 
    in the showing section in the strategy file.'''
    def __init__(self,section:str,parameter:str):
        '''
        Args:
            section: A `str` indicates the section of the missing parameter.
            parameter: A `str` indicates the name of the missing parameter.
        '''
        indication = f'Missing `{parameter}` parameter in `{section}` section '\
            'in strategy file.'
        super().__init__(indication)

## ================================= `Crash` Error ================================= ##
class StrategyCrashError(StrategyError):
    '''This exception indicates the attempting 
    to load extra prompt without designating prompt role.'''
    def __init__(self):
        indication = '`prompt` parameter not provided in `chat.role` section '\
            'or being manually set via methods.\n'\
            'Extra prompt not available.'
        super().__init__(indication)

## ============================ `NoAvailableMode` Error ============================ ##
class StrategyNoAvailableModeError(StrategyError):
    '''This exception indicates neither `call` or `chat` strategy is initialized.'''
    def __init__(self):
        indication = 'Neither `call` or `chat` section is found in strategy file.'\
            'No inference mode available.\n'\
            'Note: You can not initialize strategy sections after instance creation.'
        super().__init__(indication)

## ============================== `OutOfRange` Error ============================== ##
class StrategyOutOfRangeError(StrategyError):
    '''This exception indicates the attempting to change uninitialized parameters.'''
    def __init__(self,section:Literal['call','chat']):
        '''
        Args:
            section: A given `str` indicates the name of the uninitialized section.
        '''
        indication = f'`{section}` strategy section uninitialized '\
            'due to lack of related section in strategy file.\n'\
            'You can not initialize it and modify any parameter within it '\
            'by methods during runtime.'
        super().__init__(indication)