from .classes import Section, Branch
from ....errors.components.logs import LogbaseOperationFailedError
from typing import Tuple
from sqlmodel import Session, select

## ========================== Operation `commit_record()` ========================== ##
def update_record(session:Session,
                  section:Section,branch:Branch) -> Tuple[Branch,Section]:
    '''The function is define for commit new record into logbase.
    Args:
        session: A Session class instance indicate the logbase for operation.
        section: A Section class instance indicate the section table for commitment.
        branch: A Branch class instance indicate the branch table for commitment.
    Returns:
        A tuple with Branch class instance and Section class instance 
            indicate the updated record.
    '''
    try:
        # Define search statements
        section_statement = select(Section).where(Section.id == section.id)
        branch_statement = select(Branch).where((Branch.belonging == section.id)
                                                & (Branch.id == branch.id))
        # Determined table instance
        section_obj:Section = session.exec(section_statement).first()
        branch_obj:Branch = session.exec(branch_statement).first()
        # Update log record
        if section_obj:
            section_obj.model = section.model
            section_obj.addition = section.addition
            section_obj.role = section.role
            section_obj.temperature = section.temperature
            if branch_obj:
                branch_obj.iterations = branch.iterations
                branch = branch_obj
            else:
                section_obj.branches.append(branch)
            section = section_obj
        else:
            section.branches.append(branch)
            session.add(section)
        # Commit updates
        session.commit()
        session.refresh(branch)
        session.refresh(section)
    except:
        raise LogbaseOperationFailedError()
    else:
        return branch, section
    finally:
        # Disconnet to logbase
        session.close()        

## =========================== Operation `get_section()` =========================== ##
def get_section(session:Session,id:int) -> Section | None:
    '''The function is defined for get the specific section.
    Args:
        session: A Session class instance indicate the logbase for operation.
        id: A integer indicate the identity of claimed section.
    Returns:
        A Section instance indicate the claimed section 
        or None indicate the claimed section not existed.
    '''
    try:
        statement = select(Section).where(Section.id == id)
        section = session.exec(statement=statement).first()
    except:
        raise LogbaseOperationFailedError()
    else:
        return section
    finally:
        session.close()

## =========================== Operation `get_branch()` =========================== ##
def get_branch(session:Session,section:Section,id:int) -> Branch | None:
    '''The function is defined for get the specific branch in specific section.
    Args:
        session: A Session class instance indicate the logbase for operation.
        section: A Section class instance indicate the belonging section.
        id: A integer indicate the identity of claimed branch.
    Returns:
        A Branch instance indicate the claimed branch 
        or None indicate the claimed branch not existed.
    '''
    try:
        statement = select(Branch).where((Branch.belonging == section.id) 
                                         & (Branch.id == id))
        branch = session.exec(statement).first()
    except:
        raise LogbaseOperationFailedError()
    else:
        return branch
    finally:
        session.close()

## ====================== Operation `get_latest_section_id()` ====================== ##
def get_latest_section_id(session:Session) -> int | None:
    '''The function is define for get the latest section id in logbase.
    Args:
        session: A Session class instance indicate the logbase for operation.
    Returns:
        A integer indicate current latest section id 
        or None indicate no section record has been created.
    '''
    try:
        statement = select(Section.id)
        ids = session.exec(statement=statement).all()
    except:
        raise LogbaseOperationFailedError()
    else:
        if ids:
            latest_id = max(ids)
        else:
            latest_id = None
        return latest_id  
    finally:
        session.close()

## ====================== Operation `get_latest_branch_id()` ====================== ##
def get_latest_branch_id(session:Session,section:Section) -> int | None:
    '''The function is defined for get the latest branch id in current section record.
    Args:
        session: A Session class instance indicate the logbase for operation.
        section: A Section class instance indicate the belonging section record.
    Returns:
        A integer indicate current latest branch id in current section record
        or None indicate no branch record has been created in current section record.
    '''
    try:
        statement = select(Branch.id).where(Branch.belonging==section.id)
        ids = session.exec(statement=statement).all()
    except:
        raise LogbaseOperationFailedError()
    else:
        if ids:
            latest_id = max(ids)
        else:
            latest_id = None
        return latest_id    
    finally:
        session.close()