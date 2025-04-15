import time

### =============================== Expose Class =============================== ###
class Log:
    '''The class is defined for work with model inference records'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Log class object.
        Returns:
            log: A object indicate logs of inference.
        '''
        # Initialize inference history attributes
        self.id = 0
        self.history = []

    ## =========================== Record Methods =========================== ##
    def call(self,model:str,
             role:dict,
             input:str,output:str,
             temperature:float,
             strategy:str) -> None:
        '''The method is defined for record log for single call inference.
        Args:
            model: A string indicate the name of model file
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            role: A dictionary indicate input and output role of 
                single call inference.
            temperature: A float indicate the model inference temperature.
            strategy: A string indicate the path to the strategy file.
        '''
        # Update history ID
        self.id += 1
        # Make history content of the inference
        history = {
            'id': self.id,
            'create_at': time.time(),
            'model': model,
            'role': role,
            'iteration': [{
                'query': input,
                'response': output
                }],
            'temperature': temperature,
            'strategy': strategy
            }
        # Append history attribute
        self.history.append(history)
    