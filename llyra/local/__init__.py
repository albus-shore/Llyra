from . import llama,prompt,log

class Model:
    '''The class is defined for fulfill local LLM call.'''

    ## ========================= Class Initialize Method ========================== ##
    def __init__(self,model:str=None,directory:str=None,gpu:bool=None) -> object:
        '''The method is defined for initialize model object.
        Args:
            model: A string indicate the model file,
                which should be placed in './model/' by default.
            directory: A string indicate the folder of model file.
            gpu: A bool indicate whether use GPU for acceleration.
        Returns:
            A target LLM loaded Model object.
        '''
        # Load necessary modules
        from . import config
        # Import toolkit config
        config_path = 'config/config.json'
        self.model, self.directory, self.gpu = config.load(config_path)
        # Update config parameter by input
        if model:
            self.model = config.name(model)
        if directory:
            self.directory = config.folder(directory)
        if gpu:
            self.gpu = gpu
        # Make model object attribute
        self.LLM = llama.initialize(self.model,
                                         self.directory,
                                         self.gpu)
        # Initialize history attributea
        self.query:str
        self.response:str
        self.history:list = []

    ## ========================== Call Method ========================== ##
    def call(self,message:str,
             input_role:str=None,output_role:str=None,
             stop:str=None,max_token:int=None) -> str:
        '''The method is defined for fulfill single LLM call.
        Args:
            input_role: A string indicate the role of input.
            output_role: A string indicate the role of output.
            stop: A string indicate where the model should stop generation.
        Returns:
            A string indicate the model reponse content.
        '''
        # Improt necessary module
        from . import strategy
        # Input singel infer startage
        strategy_path = 'config/strategy.json'
        role, default_stop, default_max_token = strategy.load(strategy_path)
        # Update strategy parameter by input
        if input_role:
            role['input'] = input_role
        if output_role:
            role['output'] = output_role
        if not stop:
            stop = default_stop
        if not max_token:
            max_token = default_max_token
        # Make prompt
        content = prompt.prompt(role,message)
        # Fulfill model inference
        self.response = self.LLM.create_completion(content,max_tokens=max_token,stop=stop)['choices'][0]['text']
        # Update log
        self.query = message
        record = log.record(role,message,self.response)
        self.history.append(record)
        # Return model inference response
        return self.response
