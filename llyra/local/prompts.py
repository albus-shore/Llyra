from ..base import Prompt

class PromptLocal(Prompt):
    '''The class is defind for generate prompt for local model inference.'''
    ### ============================ Dynamic Methods ============================ ###
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize PromptLocal class object.'''
        # Initialize parent class
        super().__init__()
  
    ### ============================ Static Methods ============================ ###
    ## =========================== Generate Method =========================== ##
    @staticmethod
    def call(role:dict,content:str) -> str:
        '''The method is defined for generate prompt of single call inference.
        Args: 
            role: A dictionary indicate input and output role of 
                single call inference.
            content: A string indicate the input content for model inference.
        Returns:
            prompt: A string indicate proper structed content for inference.            
        '''
        # Get single call role prompt parameters
        input = role['input'] or ''
        output = role['output'] or ''
        # Make structed prompt
        prompt = input + content + output
        # Return prompte for inference
        return prompt
    