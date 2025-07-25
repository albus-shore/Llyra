## =================================== Log Error =================================== ##
class LogError(Exception):
    '''The class is defined as the base of all custom errors of log process.'''
    pass

## =============================== Log Section Error =============================== ##
class LogSectionError(LogError):
    '''The class is defined as the base of all custom errors of log section process.'''
    pass

## ========================== Log Section Not Exist Error ========================== ##
class LogSectionNotExistError(LogSectionError):
    '''The class is defined to indicate error 
    when switching to not-created section record.'''
    def __init__(self,id:int):
        '''
        Args:
            id: A integer indicate the claimed section record.
        '''
        indication = f'Section `{id}` not existed.'
        super().__init__(indication)

## =========================== Log Section Not Set Error =========================== ##
class LogSectionNotSetError(LogSectionError):
    '''The class is defined to indicate error 
    when executing section-required operations without setting specific section.'''
    def __init__(self):
        indication = 'Section has not been set.'
        super().__init__(indication)

## =============================== Log Branch Error =============================== ##
class LogBranchError(LogError):
    '''The class is defined as the base of all custom errors of log branch process.'''
    pass

## ========================== Log Branch Not Exist Error ========================== ##
class LogBranchNotExistError(LogBranchError):
    '''The class is defined to indicate error 
    when switching to not-created branch record in current section.'''
    def __init__(self,id:int,belonging:int):
        '''
        Args:
            id: A integer indicate the claimed branch record.
            belonging: A integer indicate the belonging section 
                of the claimed branch record.
        '''
        indication = f'Branch `{id}` not existed in Section `{belonging}`.'
        super().__init__(indication)

## =========================== Log Branch Not Set Error =========================== ##
class LogBranchNotSetError(LogBranchError):
    '''The class is defined to indicate error 
    when executing branch-required operations without setting specific branch.'''
    def __init__(self):
        indication = 'Branch has not been set.'
        super().__init__(indication)

## ====================== Log Branch Parent Not Specify Error ====================== ##
class LogBranchParentNotSpecifyError(LogBranchError):
    '''The class is defined to indicate error
    when creating new branch without specifying its parent branch record.'''
    def __init__(self):
        indication = 'Parent branch record not specified for new branch creation.'
        super().__init__(indication)

## ================================= LogBase Error ================================= ##
class LogBaseError(LogError):
    '''The class is defined as the base of all custom errors of logbase process.'''
    pass

## ========================= LogBase Format Invalid Error ========================= ##
class LogBaseFormatInvlidError(LogBaseError):
    '''The class is defined to indicate error 
    when the format of record in logbase is invalid.'''
    def __init__(self):
        indication = 'Logbase format not compatible.'
        super().__init__(indication)

## =============================== Log Record Error =============================== ##
class LogRecordError(LogError):
    '''The class is defined as the base of all custom errors 
    of log recording process.'''
    pass

## =========================== Log Inference Type Error =========================== ##
class LogInferenceTypeError(LogRecordError):
    '''The class is defined to indicate error when log record operation is invalid 
    under the inference type of current section.'''
    def __init__(self):
        indication = 'Inference type not compatible.'
        super().__init__(indication)
