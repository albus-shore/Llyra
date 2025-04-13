### =============================== Expose Class =============================== ###
class Prompt():
    '''The class is defind for generate prompt for model inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Prompt class object.
        Returns:
            prompt: A object indicate prompt for inference.
        '''
        # Initialize single call prompt build parameter attributes
        self.call_input:str = None
        self.call_output:str = None

    ## ============================= Set Mothod ============================= ##
    def set(self,call:dict) -> None:
        '''The method is defined for set prompt parameters with input.
        Args:
            call: A dictionary indicate input and output role of 
                single call inference.
        '''
        # Set single call prompt parameters
        self.call_input = call['input']
        self.call_output = call['output']

    ## ========================== Generate Methods ========================== ##
    def call(self,content:str) -> str:
        '''The method is defined for generate prompt of single call inference.
        Args: 
            content: A string indicate the input content for model inference.
        Returns:
            prompt: A string indicate proper structed content for inference.            
        '''
        # Make structed prompt
        prompt = self.call_input + content + self.call_output
        # Return prompte for inference
        return prompt