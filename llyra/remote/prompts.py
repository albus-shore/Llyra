from ..base import Prompt

class PromptRemote(Prompt):
    '''The class is defind for generate prompt for remote model inference.'''
    ### ============================ Dynamic Methods ============================ ###
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize PromptRemote class object.'''
        # Initialize parent class
        super().__init__()

    ### ============================ Static Methods ============================ ###
    ## =========================== Generate Method =========================== ##
    @staticmethod
    def call(content:str) -> str:
        '''The method is defined for generate prompt of single call inference.
        Args: 
            content: A string indicate the input content for model inference.
        Returns:
            prompt: A string indicate proper structed content for inference.            
        '''
        # Make structed prompt
        prompt = content
        # Return prompte for inference
        return prompt    