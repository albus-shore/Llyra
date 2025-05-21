from ..base import Log

### =============================== Expose Class =============================== ###
class LogLocal(Log):
    '''The class is defined for work with model inference records'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize LogLocal class object.'''
        # Initialize parent class
        super().__init__()

    ## =========================== Record Methods =========================== ##
    def call(self,model:str,
             role:dict,
             input:str,output:str,
             temperature:float) -> None:
        '''The method is defined for record log for single call inference.
        Args:
            model: A string indicate the name of model file
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            role: A dictionary indicate input and output role of 
                single call inference.
            temperature: A float indicate the model inference temperature.
        '''
        super()._call(model,input,output,
                      role=role,temperature=temperature)

    def chat(self,model:str,
             prompt:str,
             role:dict,
             input:str,output:str,
             temperature:float,
             keep:bool) -> None:
        '''The method is defined for record log for iterative chat inference.
        Args:
            model: A string indicate the name of model file.
            prompt: A string indicate the content of additional prompt.
            role: A dictionary indicate input and output role of
                iterative chat inference.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.
            keep: A boolean indicate whether continue the iteration.
        '''
        super()._chat(model,
                      prompt,
                      role,
                      input,output,
                      keep,
                      temperature=temperature)