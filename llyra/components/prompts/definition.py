from .utils import make_new_inference
from ..utils import Role

class Prompt():
    '''The class is defined to define universal attributes and methods,
    for generating prompts for model inference..'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined for initialize Prompt class object.'''
        # Initialize chat iteration attribute
        self._iteration:list = []

    ## ============================= Generate Methods ============================= ##
    def call(self,content:str) -> str:
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

    def chat(self,role:Role,content:str,addition:str) -> list:
        '''The method is defined for generate prompt of iterative chat inference.
        Args:
            role: A dataclass indicate input and prompt role of
                iterative chat inference.
            content: A string indicate the input content for model inference.
            addition: A string indicate additional prompt for model inference.
        Returns:
            prompt: A list indicate proper structed content for chat inference.
        '''
        # Get iterative chat role prompt parameters
        prompt = role.prompt
        input = role.input
        # Get iteration record
        iteration_prompt = self._iteration[:]
        # Discrinimate whether and how to add additional prompt
        if addition:
            additional_prompt = make_new_inference(role=prompt,
                                                   content=addition)
            iteration_prompt.insert(0,additional_prompt)
        # Make structed prompt
        user_prompt = make_new_inference(role=input,content=content)
        iteration_prompt.append(user_prompt)
        # Return prompt for inference
        return iteration_prompt
    
    ## ======================== Additional Method for Chat ======================== ##
    def iterate(self,role:Role,input:str,output:str,keep:bool) -> None:
        '''The method is defined for update chat iteration history record.
        Args:
            role: A dataclass indicate the input and output role of 
                the iteration record.
            input: A string indicate the input content of the iteration record.
            output: A string indicate the output content of the iteration record.
            keep: A boolean indicate whether continue last chat iterarion.
        '''
        # Discriminate whether continue last chat iteration
        if not keep:
            self._iteration = []
        # Discriminate whether make new iteration records
        if role == None:
            return
        # Append input record to iteration record attribute
        if input:
            input_record = make_new_inference(role.input,input)
            self._iteration.append(input_record)
        # Append output record to iteration record attribute
        if output:
            output_record = make_new_inference(role.output,output)
            self._iteration.append(output_record)