### ============================= Inside Functions ============================= ###
def make(role:str,content:str) -> dict:
    '''The function is defined for make single prompt record in chat iteration.
    Args:
        role: A string indicate the role of the content.
        content: A sting indicate the content of the prompt record.
    Returns:
        A dictionary indicate the single prompt record in chat iteration.
    '''
    # Make single prompt dictionary
    single_prompt = {role: content}
    # Return single prompt dictionary
    return single_prompt


### =============================== Expose Class =============================== ###
class Prompt():
    '''The class is defind for generate prompt for model inference.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Prompt class object.
        Returns:
            prompt: A object indicate prompt for inference.
        '''
        # Initialize chat iteration attribute
        self.iteration:list = []

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
        prompt_role = role['prompt']
        input_role = role['input']
        # Get iteration record
        prompt = self.iteration[:]
        # Discrinimate whether add additional prompt
        if addition:
            additional_prompt = make(prompt_role,addition)
            prompt.append(additional_prompt)
        # Make structed prompt
        user_prompt = make(input_role,content)
        prompt.append(user_prompt)
        # Return prompt for inference
        return prompt

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
            last_record = make(role=role,content=content)
            # Append iteration record attribute
            self.iteration.append(last_record)