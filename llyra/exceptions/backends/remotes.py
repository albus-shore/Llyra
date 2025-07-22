## ================================= Remote Error ================================= ##
class RemoteError(Exception):
    '''The class is defined as the base of all custom errors of process of remote.'''
    pass

## ======================== Remote Server Connection Error ======================== ##
class RemoteServerConnectionError(RemoteError):
    '''The class is defined for indicate error
    when failed to connect with claimed remote server.'''
    def __init__(self):
        indication = "Can't connect to server."
        super().__init__(indication)

## ====================== Remote Service Not Compatible Error ====================== ## 
class RemoteServiceNotCompatibleError(RemoteError):
    '''The class is defined for indicate error
    when failed to find compatible service on remote server
    after connecting to remote server successfully.'''
    def __init__(self):
        indication = "Can't find compatible service."
        super().__init__(indication)       

## ============================= Remote Service Error ============================= ##
class RemoteServiceError(RemoteError):
    '''The class is defined for indicate error 
    when remote service return error message 
    after connecting to remote server and finding compatible service successfully.'''
    def __init__(self,message:str):
        '''
        Args:
            message: A string indicate the error message remote service return.
        '''
        super().__init__(message)        

## ======================= Remote Model Not Available Error ======================= ##
class RemoteModelNotAvailableError(RemoteError):
    '''The class is defined for indicate error 
    when claimed model not available on remote server.'''
    def __init__(self,model):
        '''
        Args:
            model: A string indicate the name of unavailable model on remote server.
        '''
        indication = f'`{model}` not available on remote server.'
        super().__init__(indication)
