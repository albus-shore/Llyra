### =============================== Expose Class =============================== ###
class Prompt():
    '''The class is defind for generate prompt for model inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Prompt class object.
        Returns:
            prompt: A object indicate prompt for inference.
        '''
        # Initialize model inference indication attributes
        self.begin:str = None
        self.end:str = None
        # Initialize single call prompt build parameter attributes
        self.call_input:str = None
        self.call_output:str = None
    ## ============================ Config Method ============================ ##
    def config(self,indicate:dict) -> None:
        '''The method is defined for set prompt config parameters with input.
        Args:
            indicate: A dictionary indicate begin and end of content 
                indicate token for model inference.
        '''
        # Set model inference indication attributes
        self.begin = indicate['begin']
        self.end = indicate['end']

    ## ============================= Set Method ============================= ##
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
        prompt = self.begin or ''
        prompt += self.call_input or ''
        prompt += content 
        prompt += self.call_output or ''
        prompt += self.end or ''
        # Return prompte for inference
        return prompt