from .utils import make_new_inference

class Prompt():
    '''The class is defined to define basic attributes and internal methods,
    for generating prompts for model inference..'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize Prompt class object.'''
        # Initialize chat iteration attribute
        self.iteration:list = []

    ## ========================== Generate Methods ========================== ##
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
        iteration_prompt = self.iteration[:]
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
    
    ## ===================== Additional Method for Chat ===================== ##
    def iterate(self,role:str,content:str,keep:bool) -> None:
        '''The method is defined for update chat iteration history record.
        Args:
            role: A string indicate the role of the content.
            content: A sting indicate the content of the iteration record.
            keep: A boolean indicate whether continue last chat iterarion.
        '''
        # Discriminate whether continue last chat iteration
        if not keep:
            self.iteration = []
        # Discriminate whether make new iteration record
        if role != None and content !=None:
            # Make the prompt record dictionary
            last_record = make_new_inference(role=role,content=content)
            # Append iteration record attribute
            self.iteration.append(last_record)