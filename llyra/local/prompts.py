### =============================== Expose Class =============================== ###
class Prompt():
    '''The class is defind for generate prompt for model inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Prompt class object.
        Returns:
            prompt: A object indicate prompt for inference.
        '''

    ## ========================== Generate Methods ========================== ##
    def call(self,role:dict,content:str) -> str:
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