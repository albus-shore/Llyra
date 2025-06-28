from sqlmodel import SQLModel, Field, Relationship
from dataclasses import dataclass
from time import time

## =========================== Data Class `Iteration()` =========================== ##
@dataclass
class Iteration:
    '''The class is defined for managing iteration record in branch record.
    Args:
        query: A string indicate input content for model inference.
        response: A string indicate response of model inference.
    '''
    query: str
    response: str
    
## ============================ Table Class `Branch()` ============================ ##
class Branch(SQLModel, table=True):
    '''The class is defined for managing branch record in section record.
    Args:
        id: A integer indicate the identity of current branch record.
        belonging: A integer indicate the belonging section of the branch record.
    '''
    # Keys
    id: int = Field(primary_key=True)
    belonging: int = Field(foreign_key='section.id',primary_key=True)
    iterations: str
    # ORM Link
    section: "Section" = Relationship(back_populates='branches')

## ============================ Table Class `Section()` ============================ ##
class Section(SQLModel, table=True):
    '''The class is defined for manageing section record.
    Args:
        id: A integer indicate the identity of current section record.
        model: A string indicate the name of model.
        addition: A string indicate the content of additional prompt.
        role: A daraclass indicate input, output, and prompt role of 
            interative chat inference.
        temperature: A float indicate the model inference temperature.
    '''
    # Keys
    id: int = Field(primary_key=True)
    type: str
    model: str
    addition: str | None
    role: str | None
    temperature: float
    create_at: float = Field(default_factory=time)
    # ORM Link
    branches: list[Branch] = Relationship(back_populates='section')