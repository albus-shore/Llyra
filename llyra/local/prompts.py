from ..base.prompts import Prompt

class PromptLocal(Prompt):
    '''The class is defind for generate prompt for local model inference.'''
    ### ============================ Dynamic Methods ============================ ###
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize PromptLocal class object.'''
        # Initialize parent class
        super().__init__()

    ## =========================== Generate Method =========================== ##
    def chat(self,role:dict,content:str,addition:str) -> list:
        '''The method is defined for generate prompt of iterative chat inference.
        Args:
            role: A dictionary indicate input and prompt role of
                iterative chat inference.
            content: A string indicate the input content for model inference.
            addition: A string indicate additional prompt for model inference.
        Returns:
            prompt: A list indicate proper structed content for chat inference.
        '''
        # Get iterative chat role prompt parameters
        prompt = role['prompt']
        input = role['input']
        # Get iteration record
        iteration_prompt = self._iteration[:]
        # Discrinimate whether add additional prompt
        if addition:
            additional_prompt = self.make(prompt,addition)
            iteration_prompt.insert(0,additional_prompt)
        # Make structed prompt
        user_prompt = self.make(input,content)
        iteration_prompt.append(user_prompt)
        # Return prompt for inference
        return iteration_prompt
    
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
    