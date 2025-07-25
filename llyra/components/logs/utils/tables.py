from sqlmodel import SQLModel, Field, Relationship

## ========================= Table Class `TableSection()` ========================= ##
class TableSection(SQLModel, table=True):
    '''The class is defined for operating with section records in SQL database.
    Args:
        id: A integer indicate the identity of current section record.
        type: A string indicate the inference mode of current section record.
        model: A string indicate the name of inference model.
        addition: A string indicate the content of additional prompt.
        role: A json string indicate input, output, and prompt role of
            iterative chat inference.
        temperature: A float indicate the model inference temperature.
    '''
    id: int = Field(primary_key=True)
    type: str
    model: str
    addition: str | None
    role: str | None
    temperature: float
    create_at: float

    # ORM link
    branches: list['TableBranch'] = Relationship(back_populates='section')

## ========================== Table Class `TableBranch()` ========================== ##
class TableBranch(SQLModel, table=True):
    '''The class is defined for operating with branch records in SQL database.
    Args:
        id: A integer indicate the identity of current branch record.
        belonging: A integer indicate the belonging section of current branch record.
        iterations: A json list string 
            indicate the inference history of current branch record.
    '''
    id: int = Field(primary_key=True)
    belonging: int = Field(foreign_key='tablesection.id',primary_key=True)
    iterations: str

    # ORM link
    section: TableSection = Relationship(back_populates='branches')