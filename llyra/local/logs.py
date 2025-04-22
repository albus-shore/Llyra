import time

### ============================= Inside Functions ============================= ###
def new(id:int,
        model:str,
        prompt:str,
        role:dict,
        temperature:float,
        strategy:str,
        ) -> dict:
    '''The function is defined for make new chat history record dictionary.
    Args:
        id: A integrate indicate the identity of current chat log.
        model: A string indicate the name of model file.
        prompt: A string indicate the content of additional prompt.
        role: A dictionary indicate input and output role of
                iterative chat inference.
        temperature: A float indicate the model inference temperature.
        strategy: A string indicate the path to the strategy file.
    Returns:
        history: A dictionary indicate the basic information of 
            the chat iteration.
    '''
    history = {
        'id': id,
        'type': 'chat',
        'create_at': time.time(),
        'model': model,
        'prompt': prompt,
        'role': role,
        'iteration':[],
        'temperature': temperature,
        'strategy': strategy,
            }
    return history

### =============================== Expose Class =============================== ###
class Log:
    '''The class is defined for work with model inference records'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> object:
        '''The method is defined for initialize Log class object.
        Returns:
            log: A object indicate logs of inference.
        '''
        # Initialize inference history attributes
        self.id = 0
        self.history = []

    ## =========================== Record Methods =========================== ##
    def call(self,model:str,
             role:dict,
             input:str,output:str,
             temperature:float,
             strategy:str) -> None:
        '''The method is defined for record log for single call inference.
        Args:
            model: A string indicate the name of model file
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            role: A dictionary indicate input and output role of 
                single call inference.
            temperature: A float indicate the model inference temperature.
            strategy: A string indicate the path to the strategy file.
        '''
        # Update history ID
        self.id += 1
        # Make history content of the inference
        history = {
            'id': self.id,
            'type': 'call',
            'create_at': time.time(),
            'model': model,
            'role': role,
            'iteration': [{
                'query': input,
                'response': output
                }],
            'temperature': temperature,
            'strategy': strategy
            }
        # Append history attribute
        self.history.append(history)
    
    def chat(self,model:str,
             prompt:str,
             role:dict,
             input:str,output:str,
             temperature:float,
             strategy:str,
             keep:bool) -> None:
        '''The method is defined for record log for iterative chat inference.
        Args:
            model: A string indicate the name of model file.
            prompt: A string indicate the content of additional prompt.
            role: A dictionary indicate input and output role of
                iterative chat inference.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.
            strategy: A string indicate the path to the strategy file.
            keep: A boolean indicate whether continue the iteration.
        '''
        # Discriminate whether continue the iteration
        if keep and self.history:
            if self.history[-1]['type'] == 'chat':
                history = self.history.pop(-1)
            else:
                # Update history ID
                self.id += 1
                # Make history content of the inference
                history = new(id=self.id,
                              model=model,
                              prompt=prompt,
                              role=role,
                              temperature=temperature,
                              strategy=strategy)
        else:
            # Update history ID
            self.id += 1
            # Make history content of the inference
            history = new(id=self.id,
                          model=model,
                          prompt=prompt,
                          role=role,
                          temperature=temperature,
                          strategy=strategy)
        # Make iteration content
        iteration = {
            'query': input,
            'response': output,
            }
        # Append history intertion
        history['iteration'].append(iteration)
        # Append history attribute
        self.history.append(history)