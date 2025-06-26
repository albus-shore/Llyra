## ================================ Strategy Error ================================ ##
class StrategyError(Exception):
    '''The class is defined as the base of all custom errors of strategy process.'''
    pass

## ============================= Section Missing Error ============================= ##
class StrategySectionMissingError(StrategyError):
    '''The class is defined for indicate error 
    when strategy file missing necessary sections.'''
    def __init__(self,section:str):
        '''
        Args:
            section: A string indicate the missing section in strategy file.
        '''
        indication = f'Missing `{section}` section in `strategy.toml`.'
        super().__init__(indication)

## ============================ Parameter Missing Error ============================ ##
class StrategyParameterMissingError(StrategyError):
    '''The class is defined for indicate error 
    when strategy file missing necessary parameters.'''
    def __init__(self,section:str,parameter:str):
        '''
        Args:
            section: A string indicate the belonging section of the missing parameter.
            parameter: A string indicate the missing parameter in strategy file.
        '''
        indication = f'Missing `{parameter}` parameter of `{section}` section '
        indication += 'in `strategy.toml`.'
        super().__init__(indication)