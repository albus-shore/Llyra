## =================================== Log Error =================================== ##
class LogError(Exception):
    '''The class is defined as the base of all custom error of log operation.'''
    pass

## ========================= Log Section Not Created Error ========================= ##
class LogSectionNotCreatedError(LogError):
    '''The class is defined for indicate error 
    when user try to get a section which hasn't been created.'''
    def __init__(self,id:int):
        '''
        Args:
            id: A integer indicate the claimed section.
        '''
        indication = f"Section `{id}` hasn't been created."
        super().__init__(indication)

## ========================= Log Branch Not Created Error ========================= ##
class LogBranchNotCreatedError(LogError):
    '''The class is defined for indicate error 
    when user try to get a branch which hasn't been created in current section.'''
    def __init__(self,section:int,branch:int):
        '''
        Args:
            section: A integer indicate the belonging section of claimed branch.
            branch: A integer indicate the claimed branch.
        '''
        indication = f"Branch `{branch}` hasn't been created in Section `{section}`."
        super().__init__(indication)

## =========================== Log Section Not Set Error =========================== ##
class LogSectionNotSetError(LogError):
    '''The class is defined for indicate error
    when user try to execute operations need section be set without setting section.'''
    def __init__(self):
        indication = "Section hasn't been set."
        super().__init__(indication)        

## =========================== Log Branch Not Set Error =========================== ## 
class LogBranchNotSetError(LogError):
    '''The class is defined for indicate error
    when user try to execute operations need branch be set without setting section.'''
    def __init__(self):
        indication = "Branch hasn't been set."
        super().__init__(indication)       

## =========================== Log Inference Mode Error =========================== ##
class LogInferenceModeError(LogError):
    '''The class is defined for indicate error
    when user try to execute record operation in invalid way of inference mode.'''
    def __init__(self):
        indication = "Inference mode not compatible."
        super().__init__(indication)

## ======================== Logbase Operation Failed Error ======================== ##
class LogbaseOperationFailedError(LogError):
    '''The class is defined for indicate error
    when logbase operation failed.'''        
    pass