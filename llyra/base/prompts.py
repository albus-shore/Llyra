class Prompt():
    '''The class is defined to define basic attributes and internal methods,
    for generating prompts for model inference..'''
    ### ============================ Dynamic Methods ============================ ###
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initialize Prompt class object.'''
        # Initialize chat iteration attribute
        self._iteration:list = []

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
        # Discrinimate whether and how to add additional prompt
        if addition:
            additional_prompt = self.make(prompt,addition)
            iteration_prompt.insert(0,additional_prompt)
        # Make structed prompt
        user_prompt = self.make(input,content)
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
            self._iteration = []
        # Discriminate whether make new iteration record
        if role != None and content !=None:
            # Make the prompt record dictionary
            last_record = self.make(role=role,content=content)
            # Append iteration record attribute
            self._iteration.append(last_record)

    ### ============================ Static Methods ============================ ###
    ## ======================== Internal Make Method ======================== ##
    @staticmethod
    def make(role:str,content:str) -> dict:
        '''The function is defined for make single prompt record in chat iteration.
        Args:
            role: A string indicate the role of the content.
            content: A sting indicate the content of the prompt record.
        Returns:
            A dictionary indicate the single prompt record in chat iteration.
        '''
        # Make single prompt dictionary
        prompt = {'role':role,'content': content}
        # Return single prompt dictionary
        return prompt            