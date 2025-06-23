class ModelNotAvailableError(Exception):
    '''The class is defined for indicate error 
    when claimed model not available on remote server.'''
    def __init__(self,model):
        '''
        Args:
            model: A string indicate the name of unavailable model on remote server.
        '''
        indication = f'`{model}` not available on remote server.'
        super().__init__(indication)
