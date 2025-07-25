from .utils import TableSection, TableBranch
from .utils import convert2Role, convert2Iteration_list, convert2json_list, convert2json
from .utils import Record
from ..utils import Role
from ...utils import Iteration, Branch, Section
from ...exceptions.components.logs import LogSectionNotExistError, LogSectionNotSetError
from ...exceptions.components.logs import LogBranchNotExistError, LogBranchNotSetError, LogBranchParentNotSpecifyError
from ...exceptions.components.logs import LogInferenceTypeError
from sqlmodel import Session, select
from copy import deepcopy

class Log:
    '''The class is defined to define universal attributes and methods,
    for working with logs.'''
    ## ============================= Initialize Method ============================= ##
    def __init__(self) -> None:
        '''The method is defined to initialize Log class object.'''
        # Define inference record attributes
        self.section: Section = None
        self.branch: Branch = None
        # Define database engine attribute
        self._engine = None

    ## ================================ Load Method ================================ ##
    def load(self,engine) -> None:
        '''The method is defined to load database engine for database operation.
        Args:
            engine: A Engine class instance indicate the database engine.
        '''
        # Load database engine attribute
        self._engine = engine

    ## ==================== Section & Branch Operation Methods ==================== ##
    def create_section(self) -> tuple[Section, Branch]:
        '''The method is defined to create new section and default branch associated.
        Returns:
            (section, branch): 
                A Section dataclass instance 
                    indicate the new section for recording.\n
                A Branch dataclass instance 
                    indicate the default branch of the new section for recording.
        '''
        # Get section records' ids
        with Session(self._engine) as logbase:
            statement = select(TableSection.id)
            ids = logbase.exec(statement).all()                
        # Determind new section's id
        if ids:
            new_id = max(ids) + 1
        else:
            new_id = 0
        # Create new section
        self.section = Section(id=new_id,
                               type=None,
                               model=None,
                               addition=None,
                               role=None,
                               temperature=None)
        # Create default branch associated
        self.branch = Branch(id=0,
                             belonging=self.section.id)
        # Return current section and branch
        return (self.section, self.branch)

    def switch_section(self,id:int) -> tuple[Section, None]:
        '''The method is defined to switch to specific section record in logbase.
        Args:
            id: A integer indicate the section record switch to.
        Returns:
            (section, None):
                A Section dataclass instance indicate the current section record.\n
                A None object to reset current branch record for specifying.
        '''
        # Get section record data
        with Session(self._engine) as logbase:
            ## Get section record
            statement = select(TableSection).where(TableSection.id == id)
            section = logbase.exec(statement).first()
            ## Convert database record to runtime data
            if section:
                self.section = Section(id=section.id,
                                        type=section.type,
                                        model=section.model,
                                        addition=section.addition,
                                        role=convert2Role(section.role),
                                        temperature=section.temperature,
                                        create_at=section.create_at)
            ## Raise exception
            else:
                raise LogSectionNotExistError(id)
        # Reset branch attribute
        self.branch = None
        # Return current section and branch
        return (self.section, self.branch)

    def switch_branch(self,id:int) -> Branch:
        '''The method is defined to switch to specific branch record 
        of current section record in logbase.
        Args:
            id: A integer indicate the branch switch to.
        Returns:
            branch:
                A Branch dataclass instance indicate the current branch record. 
        '''
        # Discriminate whether the belonging section has been set
        if not self.section:
            raise LogSectionNotSetError()
        # Get branch record data
        with Session(self._engine) as logbase:
            ## Get branch record
            statement = select(TableBranch).where(
                (TableBranch.belonging == self.section.id)
                & (TableBranch.id == id)
                )
            branch = logbase.exec(statement).first()
            ## Convert database record to runtime data
            if branch:
                self.branch = Branch(id=branch.id,
                    belonging=branch.belonging,
                    iterations=convert2Iteration_list(branch.iterations))
            ## Raise exception
            else:
                raise LogBranchNotExistError(id=id,
                                             belonging=self.section.id)
        # Return current branch
        return self.branch

    def create_branch(self) -> Branch:
        '''The method is defined to create new branch from current branch record 
        in current section record.
        Returns:
            branch:
                A Branch dataclass instance indicate the new branch for recording.
        '''
        # Discriminate whether the belonging section has been set
        if not self.section:
            raise LogSectionNotSetError()
        # Discriminate whether the parent branch record has been set
        if not self.branch:
            raise LogBranchParentNotSpecifyError()
        # Get branch records' ids
        with Session(self._engine) as logbase:
            statement = select(TableBranch.id).where(
                TableBranch.belonging == self.section.id
                )
            ids = logbase.exec(statement).all()
        # Determind new branch's id
        if ids:
            new_id = max(ids) + 1
        else:
            new_id = 0
        # Copy parent iteration history
        iterations = deepcopy(self.branch.iterations)
        # Create new branch
        self.branch = Branch(id=new_id,
                             belonging=self.section.id,
                             iterations=iterations)
        # Return current branch
        return self.branch
    
    ## ============================== Record Methods ============================== ##
    def call(self,model:str,
              input:str,output:str,
              temperature:float
              ) -> None:
        '''The method is defined to record basic log for single call inference.
        Args:
            model: A string indicate the name of model file.
            input: A string indicate input content for model inference.
            output: A string indicate response of model inference.
            temperature: A float indicate the model inference temperature.
        '''
        # Discriminate whether the section has been set
        if not self.section:
            raise LogSectionNotSetError()
        # Discriminate whether the branch has been set
        if not self.branch:
            raise LogBranchNotSetError()
        # Discriminate whether the inference type compatible
        if (self.section.type not in ('call', None)) or self.branch.iterations:
            raise LogInferenceTypeError()
        # Make branch record
        self.branch.iterations.append(Iteration(query=input,response=output))
        # Make inference parameters record
        self.section.type = 'call'
        self.section.model = model
        self.section.temperature = temperature
        # Write record into logbase
        with Session(self._engine) as logbase:
            ## Create new section record
            section = TableSection(id=self.section.id,
                                    type=self.section.type,
                                    model=self.section.model,
                                    addition=None,
                                    role=None,
                                    temperature=self.section.temperature,
                                    create_at=self.section.create_at)
            logbase.add(section)
            ## Make new branch record
            branch = TableBranch(id=self.branch.id,
                                 belonging=self.branch.belonging,
                                 iterations=convert2json_list(self.branch.iterations))    
            section.branches.append(branch)
            ## Commit logbase change
            logbase.commit()

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
        # Discriminate whether the section has been set
        if not self.section:
            raise LogSectionNotSetError()
        # Discriminate whether the branch has been set
        if not self.branch:
            raise LogBranchNotSetError()
        # Discriminate whether the inference type compatible
        if self.section.type not in ('chat', None):
            raise LogInferenceTypeError()
        # Make branch record
        self.branch.iterations.append(Iteration(query=input,response=output))
        # Make inference parameters record
        self.section.type = 'chat'
        self.section.model = model
        self.section.addition = addition
        self.section.role = role
        self.section.temperature = temperature
        # Write record into logbase
        with Session(self._engine) as logbase:
            ## Get the section record
            section_statement = select(TableSection).where(
                TableSection.id == self.section.id
                )
            section = logbase.exec(section_statement).first()
            ## Update existed section record
            if section:
                section.model = self.section.model
                section.addition = self.section.addition
                section.role = convert2json(self.section.role)
                section.temperature = self.section.temperature
            ## Create new section record
            else:
                section = TableSection(id=self.section.id,
                                       type=self.section.type,
                                       model=self.section.model,
                                       addition=self.section.addition,
                                       role=convert2json(self.section.role),
                                       temperature=self.section.temperature,
                                       create_at=self.section.create_at)
                logbase.add(section)
            ## Get the branch record
            branch_statement = select(TableBranch).where(
                (TableBranch.id == self.branch.id)
                & (TableBranch.belonging == self.section.id)
                )
            branch = logbase.exec(branch_statement).first()
            ## Update existed branch record
            if branch:
                branch.iterations = convert2json_list(self.branch.iterations)
            ## Make new branch record
            else:
                branch = TableBranch(id=self.branch.id,
                    belonging=self.branch.belonging,
                    iterations=convert2json_list(self.branch.iterations))
                section.branches.append(branch)
            ## Commit logbase change
            logbase.commit()

## ============================== Record Read Method ============================== ##
    def get(self,section:int,branch:int) -> Record:
        '''The method is defined to get specific log record in runtime.
        Args:
            section: A integer indicate the section of the log record.
            branch: A integer indicate the branch of the log record.
        Returns:
            record:
                A Record dataclass instance indicate the claimed log record.
        '''
        # Get record from logbase
        with Session(self._engine) as logbase:
            ## Get section record
            section_statement = select(TableSection).where(
                TableSection.id == section
                )
            section_record = logbase.exec(section_statement).first()
            ## Discriminate whether the section record existed
            if not section_record:
                raise LogSectionNotExistError(section)
            ## Get branch record
            branch_statement = select(TableBranch).where(
                (TableBranch.id == branch)
                & (TableBranch.belonging == section)
                )
            branch_record = logbase.exec(branch_statement).first()
            ## Discriminate whether the branch record existed
            if not branch_record:
                raise LogBranchNotExistError(id=branch,belonging=section)
            ## Make log record
            record = Record(section=section_record.id,
                            type=section_record.type,
                            model=section_record.model,
                            addition=section_record.addition,
                            role=convert2Role(
                                section_record.role
                                ),
                            branch=Branch(
                                id=branch_record.id,
                                belonging=branch_record.belonging,
                                iterations=convert2Iteration_list(
                                    branch_record.iterations
                                    )
                                ),
                            temperature=section_record.temperature,
                            create_at=section_record.create_at)
        # Return log record
        return record