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
        # Initialize prompt content placeholder attributes
        self.history:str = None
        self.rag:str = None
        self.tool:str = None
        # Initialize chat prompt build parameter attributes
        self.iteration:str = ''

    ## ============================ Config Method ============================ ##
    def config(self,indicate:dict,placeholder:dict) -> None:
        '''The method is defined for set prompt config parameters with input.
        Args:
            indicate: A dictionary indicate begin and end of content 
                indicate token for model inference.
            placeholder: A dictionary indicate place of extra content 
                in chat prompt.
        '''
        # Set model inference indication attributes
        self.begin = indicate['begin']
        self.end = indicate['end']
        # Set prompt content placeholder attributes
        self.history = placeholder['history']
        self.rag = placeholder['rag']
        self.tool = placeholder['tool']

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
        # Set single call prompt parameters
        input = role['input']
        output = role['output']
        # Make structed prompt
        if input or output:
            prompt = self.begin or ''
            prompt += input or ''
            prompt += content 
            prompt += output or ''
            prompt += self.end or ''
        else:
            prompt = content
        # Return prompt for inference
        return prompt
    
    def chat(self,role:dict,content:str,
             system:str) -> str:
        '''The method is defined for generate prompt of iterative chat inference.
        Args:
            role: A dictionary indicate input and output role of 
                iterative chat inference.
            content: A string indicate the input content for model inference.
            system: A string indicate the system prompt for model inference.
        Returns:
            prompt: A string indicate proper structed content for inference.
        '''
        # Set iterative chat current prompt parameters
        input = role['input']
        output = role['output']
        # Make system prompt
        system_prompt = ''
        if system:
            history_insert = False
            prompts = system.splitlines(keepends=True)
            for split_prompt in prompts:
                match split_prompt.strip():
                    case self.history:
                        system_prompt += self.iteration + '\n'
                        history_insert = True
                    case self.rag:
                        pass
                    case self.tool:
                        pass
                    case _:
                        system_prompt += split_prompt
            if not history_insert:
                system_prompt = self.iteration + '\n' + system_prompt
        else:
            system_prompt += self.iteration
        # Make user prompt
        if input:
            user_prompt = input + '\n'
        else:
            user_prompt = ''
        user_prompt += content + '\n'
        user_prompt += output or ''
        # Make structed prompt
        if system_prompt:
            prompt = self.begin + '\n' + system_prompt + '\n' +self.end + '\n'
        else:
            prompt = ''
        prompt += self.begin + '\n' + user_prompt + '\n' + self.end
        # Return prompt for inference
        return prompt
    
    ## ===================== Additional Methods for Chat ===================== ##
    def iterate(self,role:str,iteration:str,keep:bool) -> None:
        '''The method is defined for manage iteration history for chat inference.
        Args:
            role: A string indicate the role of the iteration content.
            iteration: A string indicate the previous iteration history.
            keep: A boolean indicate whether continue the iteration.
        '''
        # Discriminate whether continue the iteration
        if not keep:
            self.iteration:str = ''
        # Make history content
        if role and self.iteration:
            content = '\n' + role
        elif role and not self.iteration:
            content = role
        else:
            content = ''
        if iteration and content:
            content += '\n' + iteration
        elif iteration and not content:
            content += iteration
        else:
            content += ''
        # Append iteration history
        self.iteration += content