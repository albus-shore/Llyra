from .utils import Section, Branch, Iteration
from .utils import convert_dataclass2json, convert_dataclasses2jsonlist, convert_jsonlist2dataclasses
from .utils import get_section, get_branch, get_latest_section_id, get_latest_branch_id
from .utils import update_record
from ..utils import Role
from ...errors.components.logs import LogSectionNotCreatedError, LogBranchNotCreatedError
from ...errors.components.logs import LogSectionNotSetError, LogBranchNotSetError
from ...errors.components.logs import LogInferenceModeError
from sqlmodel import Session
from json import loads

class Log:
    '''The class is defined to define universal attributes and methods,
    for working with logs.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self,logbase:Session) -> None:
        '''The method is defined to initialize Log class object.
        Args:
            logbase: A Session class instance indicate the logbase for operation.
        '''
        # Define logbase attribute
        self._logbase: Session = logbase
        # Define inference history attributes
        self.section: Section | None = None
        self.branch: Branch | None = None
        self.iterations: list[Iteration] | None = None

    ## ==================== Section & Branch Operation Methods ==================== ##  
    def change_section(self,id:int) -> None:
        '''The method is defined to operate with section record.
        Args:
            id: A integer indicate the section shift to.\n
                Set a negetive value to create a new section.
        '''
        # Seek the section record
        if id >= 0:
            section = get_section(session=self._logbase,id=id)
            if section:
                self.section = section
            else:
                raise LogSectionNotCreatedError(id=id)
        # Create new section record
        else:
            latest_id = get_latest_section_id(session=self._logbase)
            if latest_id == None:
                new_id = 0
            else:
                new_id = latest_id + 1
            self.section = Section(id=new_id)
        # Reset branch and iterations
        self.branch = None
        self.iterations = None

    def change_branch(self,id:int) -> None:
        '''The method is defined to operate with branch record in current section.
        Args:
            id: A integer indicate the branch shift to.\n
                Set a negetive value to create a new branch in current section.
        '''
        # Discriminate whether the belonging section has been set
        if self.section == None:
            raise LogSectionNotSetError()
        # Seek the branch record
        if id >= 0:
            branch = get_branch(session=self._logbase,section=self.section,id=id)
            if branch:
                self.branch = branch
                self.iterations = convert_jsonlist2dataclasses(branch.iterations)
            else:
                raise LogBranchNotCreatedError(section=self.section.id,branch=id)
        # Create new branch record
        else:
            latest_id = get_latest_branch_id(session=self._logbase,
                                                 section=self.section)
            if latest_id == None:
                new_id = 0
            else:
                new_id = latest_id + 1
            self.branch = Branch(id=new_id)
            self.iterations = []

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
        # Discriminate whether the inference environment has been set
        if self.section == None:
            raise LogSectionNotSetError()
        if self.branch == None:
            raise LogBranchNotSetError()
        # Discriminate whether inference model compatible
        if self.section.type not in ('call', None) or self.iterations:
            raise LogInferenceModeError()
        # Create Iteration record
        iteration = Iteration(query=input,response=output)
        # Add Iteration record to branch record
        self.iterations.append(iteration)
        self.branch.iterations = convert_dataclasses2jsonlist(self.iterations)
        # Make Section record
        self.section.type = 'call'
        self.section.model = model
        self.section.temperature = temperature
        # Update log records
        self.branch, self.section = update_record(session=self._logbase,
                                                  section=self.section,
                                                  branch=self.branch)

    def chat(self,model:str,
              addition:str,
              role:Role,
              input:str,output:str,
              temperature:float) -> None:
        '''The method is defined to record basic log for iterative chat inference.
        Args:
            model: A string indicate the name of model file.
            addition: A string indicate the content of additional prompt.
            role: A dataclass indicate input, output, and prompt role of
                iterative chat inference.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.   
        '''
        # Discriminate whether the inference environment has been set
        if self.section == None:
            raise LogSectionNotSetError()
        if self.branch == None:
            raise LogBranchNotSetError()
        # Discriminate whether inference model compatible
        if self.section.type not in ('chat', None):
            raise LogInferenceModeError()
        # Create Iteration record
        iteration = Iteration(query=input,response=output)
        # Add Iteration record to branch record
        self.iterations.append(iteration)
        self.branch.iterations = convert_dataclasses2jsonlist(self.iterations)
        # Make Section record
        self.section.type = 'chat'
        self.section.model = model
        self.section.addition = addition
        self.section.role = convert_dataclass2json(role)
        self.section.temperature = temperature
        # Update log records
        self.branch, self.section = update_record(session=self._logbase,
                                                  section=self.section,
                                                  branch=self.branch)

## ============================== Record Read Method ============================== ##
    def get(self,section:int,branch:int) -> dict | list:
        '''The method is defined to read log records in reasonable way.
        Args:
            section: A integer indicate specific section record.
            branch: A integer indicate specific branch record in specific section.
        Returns:
            A dictionary indicate the specific section record.
            Or a list of each section record's dictionary. 
        '''
        if section >= 0 and branch >= 0:
            # Get Table instance
            the_section = get_section(session=self._logbase,
                                              id=section)
            if not the_section:
                raise LogSectionNotCreatedError(id=section)
            # Discriminate whether get all branch records in the section
            the_branch= get_branch(session=self._logbase,
                                    section=the_section,id=branch)
            if not the_branch:
                raise LogBranchNotCreatedError(section=section,branch=branch)
            # Transform branch record
            branches = {
                'id': the_branch.id,
                'belonging': the_branch.belonging,
                'iterations': loads(the_branch.iterations)
                }
            # Transform section record
            readable_logs = {
                'id': the_section.id,
                'type': the_section.type,
                'model': the_section.model,
                'addition': the_section.addition,
                'role': loads(the_section.role or 'null'),
                'temperature': the_section.temperature,
                'create_at': the_section.create_at,
                'branch': branches                
                }
        else:
            raise ValueError('Invalid input.')
        # Return log record
        return readable_logs