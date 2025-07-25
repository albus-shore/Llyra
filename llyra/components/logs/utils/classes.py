from ...utils import Role
from ....utils import Branch
from dataclasses import dataclass
from typing import Literal

@dataclass
class Record:
    '''The class is defined to operate with specific log record.
    Args:
        section: A integer indicate the section of the log record.
        type: A string with fixed choices indicate the inference mode 
            of the log record.
        model: A string indicate the name of inference model.
        addition: A string indicate the content of additional prompt.
        role: A Role dataclass instance indicate input, output, and prompt role of
            iterative chat inference.
        branch: A Branch dataclass instance indicate the branch of the log record.
        temperature: A float indicate the model inference temperature.
        create_at: A float indicate create time of the section of the log record.
    '''
    section: int
    type: Literal['call','chat']
    model: str
    addition: str | None
    role: Role | None
    branch: Branch
    temperature: float
    create_at: float