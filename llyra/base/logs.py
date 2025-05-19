import time
from dataclasses import dataclass,field
from typing import Literal

### ============================== Inside function ============================== ###
def make(input:str,output:str) -> dict:
    '''The function is defined for make valid record of each iteration.
    Agrs:
        input: A string indicate input content for model inference. 
        output: A string indicate response of model inference.
    Returns:
        A dictionary indicate the record of the iteration.
    '''
    return {'query': input, 'response': output}


### ============================== Internal Class ============================== ###
@dataclass
class _New:
    '''The class is defined for making new chat history record.
    Args:
        id: A integrate indicate the identity of current chat log.
        model: A string indicate the name of model file.
        prompt: A string indicate the content of additional prompt.
        role: A dictionary indicate input and output role of
                iterative chat inference.
    '''
    id: int 
    type: Literal['call','chat']
    model: str
    prompt: str | None
    role: dict | None
    iteration: list = field(default_factory=list)
    create_at: float = field(default_factory=time.time)

### =============================== Expose Class =============================== ###
class Log:
    '''The class is defined to define basic attributes and internal methods,
    for working with logs.'''
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined to initialize Log class object.'''
        # Initialize inference history attributes
        self.id = 0
        self._history = []

    ## =========================== Record Methods =========================== ##
    def _call(self,model:str,
              input:str,output:str,
              **addition
              ) -> None:
        '''The method is defined to record bisic log for single call inference.
        Args:
            model: A string indicate the name of model file.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            addition: Keyword arguments indicate addition parameters. 
                needed to be record.
        '''
        # Make history content of the inference
        new_record = _New(self.id,'call',model,None,None)
        if addition:
            for attribute, value in addition.items():
                setattr(new_record,attribute,value)
        new_iteration = make(input,output)
        new_record.iteration.append(new_iteration)
        # Append history attribute
        self._history.append(new_record)
        # Update history ID
        self.id += 1

    def _chat(self,model:str,
              prompt:str,
              role:dict,
              input:str,output:str,
              keep:bool,
              **addition) -> None:
        '''The method is defined to record basic log for iterative chat inference.
        Args:
            model: A string indicate the name of model file.
            prompt: A string indicate the content of additional prompt.
            role: A dictionary indicate input and output role of
                iterative chat inference.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            addition: Keyword arguments indicate addition parameters.
            keep: A boolean indicate whether continue the iteration.     
        '''
        # Discriminate whether continue the iteration
        if self._history:
            history = self._history[-1]
        else:
            history = _New(None,None,None,None,None)
        if history.type == 'chat' and keep:
            the_record = self._history.pop(-1)
        else:
            # Make history content of the inference
            the_record = _New(self.id,'chat',model,prompt,role)
            if addition:
                for attribute, value in addition.items():
                    setattr(the_record,attribute,value)
            # Update history ID
            self.id += 1
        # Make iteration content
        new_iteration = make(input,output)
        # Append history intertion
        the_record.iteration.append(new_iteration)
        # Append history attribute
        self._history.append(the_record)

    def get(self,id:int) -> dict | list:
        '''The method is defined to read log records in reasonable way.
        Args:
            id: A integrate indicate the specific inference log.\n
                Start from 0. \n
                And read all records by set it minus.
        Returns:
            A dictionary indicate the specific log records.
            Or a list of each log record's dictionary. 
        '''
        # Discriminate whether return all log records
        if id >= 0:
            # Seek and transfrom specific log record
            try:
                the_record = self._history[id]
            except IndexError:
                raise IndexError('Error: Record not created.')
            else:
                output = vars(the_record)
        else:
            # Transform all log records
            output = []
            for record in self._history:
                output.append(vars(record))
        # Return reasonable log record
        return output
