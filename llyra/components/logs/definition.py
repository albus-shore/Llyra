from .utils import make_new_iteration, convert2readable_log, Section
from ..utils import Role
from copy import deepcopy

class Log:
    '''The class is defined to define universal attributes and methods,
    for working with logs.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined to initialize Log class object.'''
        # Initialize inference history attributes
        self.id = 0
        self._history = []

    ## ============================== Record Methods ============================== ##
    def call(self,model:str,
              input:str,output:str,
              temperature:float
              ) -> None:
        '''The method is defined to record bisic log for single call inference.
        Args:
            model: A string indicate the name of model file.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.
        '''
        # Make history content of the inference
        new_section = Section(self.id,'call',model,None,None,temperature)
        new_iteration = make_new_iteration(input,output)
        new_section.iteration.append(new_iteration)
        # Append history attribute
        self._history.append(new_section)
        # Update history ID
        self.id += 1

    def chat(self,model:str,
              addition:str,
              role:Role,
              input:str,output:str,
              temperature:float,
              keep:bool) -> None:
        '''The method is defined to record basic log for iterative chat inference.
        Args:
            model: A string indicate the name of model file.
            addition: A string indicate the content of additional prompt.
            role: A dataclass indicate input, output, and prompt role of
                iterative chat inference.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.
            keep: A boolean indicate whether continue the iteration.     
        '''
        # Discriminate whether continue the iteration
        if self._history:
            record = self._history[-1]
        else:
            record = Section(None,None,None,None,None,None)
        if record.type == 'chat' and keep:
            section = self._history.pop(-1)
        else:
            # Make history content of the inference
            section = Section(self.id,'chat',model,addition,role,temperature)
            # Update history ID
            self.id += 1
        # Make iteration content
        new_iteration = make_new_iteration(input,output)
        # Append history intertion
        section.iteration.append(new_iteration)
        # Append history attribute
        self._history.append(section)

## ============================== Record Read Method ============================== ##
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
                section = deepcopy(self._history[id])
            except IndexError:
                raise IndexError('Error: Record not created.')
            else:
                output = convert2readable_log(section)
        else:
            # Transform all log records
            output = []
            for section in self._history:
                output.append(convert2readable_log(deepcopy(section)))
        # Return reasonable log record
        return output
