import pytest
from llyra.components import Log
from llyra.components.logs.utils import TableSection, TableBranch
from llyra.components.logs.utils import Record
from llyra.components.logs.utils import convert2json_list, convert2json
from llyra.components.utils import Role
from llyra.utils import Section, Branch, Iteration
from llyra.exceptions.components.logs import LogSectionNotExistError, LogSectionNotSetError
from llyra.exceptions.components.logs import LogBranchNotExistError, LogBranchNotSetError, LogBranchParentNotSpecifyError
from llyra.exceptions.components.logs import LogInferenceTypeError

from sqlmodel import create_engine, SQLModel, Session, select

@pytest.fixture
def log():
    log = Log()
    return log

@pytest.fixture
def loaded_log():
    loaded_log = Log()
    # Create logbase engine
    engine = create_engine('sqlite://')
    # Create logbase tables
    SQLModel.metadata.create_all(engine)
    # Load logbase engine
    loaded_log.load(engine)
    return loaded_log

@pytest.fixture
def recorded_log():
    recorded_log = Log()
    # Create logbase engine
    engine = create_engine('sqlite://')
    # Create logbase tables
    SQLModel.metadata.create_all(engine)
    # Make previous record
    with Session(engine) as logbase:
        call_section_record = TableSection(
            id=0,
            type='call',
            model='test-model',
            addition=None,
            role=None,
            temperature=0.6,
            create_at=1234567.8
            )
        logbase.add(call_section_record)
        call_branch_record =TableBranch(
            id=0,
            belonging=0,
            iterations=convert2json_list(
                [Iteration('Hi','How can I help you today?')]
                )
            )
        call_section_record.branches.append(call_branch_record)
        chat_section_record = TableSection(
            id=1,
            type='chat',
            model='test-model',
            addition='This is for test.',
            role=convert2json(
                Role(prompt='system',
                     input='user',
                     output='assistant')
                ),
            temperature=0.7,
            create_at=2345678.9
            )
        logbase.add(chat_section_record)
        chat_branch_record = TableBranch(
            id=0,
            belonging=1,
            iterations=convert2json_list(
                [Iteration('Greeting!','Hi, How can I help you?')]
                )
            )
        chat_section_record.branches.append(chat_branch_record)
        logbase.commit()
    # Load logbase engine
    recorded_log.load(engine)
    return recorded_log

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(log):
    '''Test whether the class can be initialized properly.'''
    assert log.section == None
    assert log.branch == None
    assert log._engine == None

## ============================= `load()` Method Test ============================= ##
def test_load_method(log):
    '''Test whether method can load logbase engine properly.'''
    # Create logbase engine
    engine = create_engine(url='sqlite://')
    # Execute logbase engine load
    log.load(engine)
    # Validate loaded value
    assert log.section == None
    assert log.branch == None
    assert log._engine == engine

## ======================== `create_section()` Method Test ======================== ##
def test_create_section_method(loaded_log):
    '''Test whether method can create new section properly.'''
    # Create new section
    section, branch = loaded_log.create_section()
    # Set standard value
    the_section = Section(0,None,None,None,None,None,section.create_at)
    the_branch = Branch(0,0,[])
    # Validate outcome
    assert loaded_log.section == section
    assert loaded_log.branch == branch
    assert section == the_section
    assert branch == the_branch
    assert loaded_log.section == the_section
    assert loaded_log.branch == the_branch

def test_create_section_method_with_existed_record(recorded_log):
    '''Test whether method can create new section with existed record properly.'''
    # Create new section
    section, branch = recorded_log.create_section()
    # Set standard value
    the_section = Section(2,None,None,None,None,None,section.create_at)
    the_branch = Branch(0,2,[])
    # Validate outcome
    assert recorded_log.section == section
    assert recorded_log.branch == branch
    assert section == the_section
    assert branch == the_branch
    assert recorded_log.section == the_section
    assert recorded_log.branch == the_branch

## ======================== `switch_section()` Method Test ======================== ##
def test_switch_section_method(recorded_log):
    '''Test whether method can switch to specific section record 
    and reset branch record properly.'''
    # Switch to specific section
    section, branch = recorded_log.switch_section(0)
    # Set standard value
    the_section = Section(id=0,
                          type='call',
                          model='test-model',
                          addition=None,
                          role=None,
                          temperature=0.6,
                          create_at=1234567.8)
    # Validate outcome
    assert recorded_log.section == section
    assert recorded_log.branch == branch
    assert section == the_section
    assert branch == None
    assert recorded_log.section == the_section
    assert recorded_log.branch == None

def test_switch_section_method_with_not_existed_section(recorded_log):
    '''Test whether method can raise exception properly 
    when switching to not existed section.'''
    with pytest.raises(LogSectionNotExistError,match='2'):
        # Switch to specific section
        recorded_log.switch_section(2)

## ========================= `switch_branch()` Method Test ========================= ##
def test_switch_branch_method(recorded_log):
    '''Test whether method can switch to specific branch record 
    of current section record properly.'''
    # Switch to specific section
    recorded_log.switch_section(0)
    # Switch to specific branch
    branch = recorded_log.switch_branch(0)
    # Set standard value
    the_section = Section(id=0,
                          type='call',
                          model='test-model',
                          addition=None,
                          role=None,
                          temperature=0.6,
                          create_at=1234567.8)
    the_branch = Branch(id=0,
                        belonging=0,
                        iterations=[Iteration('Hi','How can I help you today?')])
    # Validate outcome
    assert recorded_log.branch == branch
    assert branch == the_branch
    assert recorded_log.branch == the_branch
    assert recorded_log.section == the_section

def test_switch_branch_method_with_not_existed_branch(recorded_log):
    '''Test whether method can raise exception properly 
    when switching to not existed branch of current section record.'''
    # Switch to specific section
    recorded_log.switch_section(0)
    # Switch to specific branch
    with pytest.raises(LogBranchNotExistError,
                       match='Branch `1` not existed in Section `0`'):
        recorded_log.switch_branch(1)

def test_switch_branch_method_without_section(recorded_log):
    '''Test whether method can raise exception properly 
    when switching branch without specifying the belonging section.'''
    # Switch to specific branch
    with pytest.raises(LogSectionNotSetError,
                       match='Section has not been set.'):
        recorded_log.switch_branch(0)

## ========================= `create_branch()` Method Test ========================= ##
def test_create_branch_method(recorded_log):
    '''Test whether method can create new branch 
    from current branch record in current section properly.'''
    # Switch to specific section
    recorded_log.switch_section(1)
    # Switch to specific branch
    recorded_log.switch_branch(0)
    # Create new branch
    branch = recorded_log.create_branch()
    # Set standard value
    the_section = Section(
        id=1,
        type='chat',
        model='test-model',
        addition='This is for test.',
        role=Role(prompt='system',
                  input='user',
                  output='assistant'),
        temperature=0.7,
        create_at=2345678.9
        )
    the_branch = Branch(
        id=1,
        belonging=1,
        iterations=[Iteration('Greeting!','Hi, How can I help you?')]
        )
    # Validate outcome
    assert recorded_log.branch == branch
    assert branch == the_branch
    assert recorded_log.section == the_section
    assert recorded_log.branch == the_branch

def test_create_branch_method_without_parent_branch(recorded_log):
    '''Test whether method can raise exception properly 
    when creating new branch without specifying parent branch record.'''
    # Switch to specific section
    recorded_log.switch_section(1)
    # Create new branch
    with pytest.raises(LogBranchParentNotSpecifyError,
        match='Parent branch record not specified for new branch creation.'):
        recorded_log.create_branch()

def test_create_branch_method_without_section(recorded_log):
    '''Test whether method can raise exception properly 
    when creating new branch without specifying the belonging section.'''
    # Create new branch
    with pytest.raises(LogSectionNotSetError,
                       match='Section has not been set.'):
        recorded_log.create_branch()

## ============================= `call()` Method Test ============================= ##
def test_call_method(loaded_log):
    '''Test whether method can make call record properly.'''
    # Create new section
    section, branch = loaded_log.create_section()
    # Make call record
    loaded_log.call(model='test-model',
                    input='test-input',output='test-response',
                    temperature=0.7)
    # Set standard value
    the_section = Section(id=0,
                          type='call',
                          model='test-model',
                          addition=None,
                          role=None,
                          temperature=0.7,
                          create_at=loaded_log.section.create_at)
    the_branch = Branch(id=0,
                        belonging=0,
                        iterations=[Iteration('test-input','test-response')])
    # Validate outcome
    assert section == loaded_log.section
    assert branch == loaded_log.branch
    assert section == the_section
    assert branch == the_branch
    assert loaded_log.section == the_section
    assert loaded_log.branch == the_branch
    with Session(loaded_log._engine) as logbase:
        section_record = logbase.exec(
            select(TableSection).where(TableSection.id == 0)
            ).first()
        assert section_record.id == the_section.id
        assert section_record.type == the_section.type
        assert section_record.model == the_section.model
        assert section_record.addition == the_section.addition
        assert section_record.role == the_section.role
        assert section_record.temperature == the_section.temperature
        assert section_record.create_at == the_section.create_at
        branch_record = logbase.exec(
            select(TableBranch).where(
                (TableBranch.id == 0) & (TableBranch.belonging == 0)
                )
            ).first()
        assert branch_record.id == the_branch.id
        assert branch_record.belonging == the_branch.belonging
        assert branch_record.iterations == convert2json_list(the_branch.iterations)

def test_call_method_with_inferred_section(recorded_log):
    '''Test whether method can raise exception properly
    when making inference record in inferred call section record.'''
    # Switch to specific section
    recorded_log.switch_section(0)
    # Switch to specific branch
    recorded_log.switch_branch(0)
    # Make call record
    with pytest.raises(LogInferenceTypeError,match='Inference type not compatible.'):
        recorded_log.call(model='test-model',
                        input='test-input',output='test-response',
                        temperature=0.7)

def test_call_method_with_chat_section(recorded_log):
    '''Test whether method can raise exception properly 
    when making call record in chat section record.'''
    # Switch to specific section
    recorded_log.switch_section(1)
    # Switch to specific branch
    recorded_log.switch_branch(0)
    # Make call record
    with pytest.raises(LogInferenceTypeError,match='Inference type not compatible.'):
        recorded_log.call(model='test-model',
                        input='test-input',output='test-response',
                        temperature=0.7)

def test_call_method_without_branch(recorded_log):
    '''Test whether method can raise exception properly 
    when making call record without specifying the belonging branch.'''
    # Switch to specific section
    recorded_log.switch_section(0)
    # Make call record
    with pytest.raises(LogBranchNotSetError,match='Branch has not been set.'):
        recorded_log.call(model='test-model',
                        input='test-input',output='test-response',
                        temperature=0.7)
        
def test_call_method_without_section(loaded_log):
    '''Test whether method can raise exception properly 
    when making call record without specifying the belonging section.'''
    # Make call record
    with pytest.raises(LogSectionNotSetError,match='Section has not been set.'):
        loaded_log.call(model='test-model',
                        input='test-input',output='test-response',
                        temperature=0.7)
        
## ============================= `chat()` Method Test ============================= ##
def test_chat_method(loaded_log):
    '''Test whether method can make chat record properly.'''
    # Create new section
    section, branch = loaded_log.create_section()
    # Make chat record
    loaded_log.chat(model='test-model',
                    addition='This is for test.',
                    role=Role(prompt='system',
                              input='user',
                              output='assistant'),
                              input='Test-Input',output='Test-Output',
                              temperature=0.6)
    # Set standard value
    the_section = Section(id=0,
                          type='chat',
                          model='test-model',
                          addition='This is for test.',
                          role=Role(prompt='system',
                                    input='user',
                                    output='assistant'),
                          temperature=0.6,
                          create_at=loaded_log.section.create_at)
    the_branch = Branch(id=0,
                        belonging=0,
                        iterations=[Iteration('Test-Input','Test-Output')]
                        )
    # Validate outcome
    assert section == loaded_log.section
    assert branch == loaded_log.branch
    assert section == the_section
    assert branch == the_branch
    assert loaded_log.section == the_section
    assert loaded_log.branch == the_branch
    with Session(loaded_log._engine) as logbase:
        section_record = logbase.exec(
            select(TableSection).where(TableSection.id == 0)
            ).first()
        assert section_record.id == the_section.id
        assert section_record.type == the_section.type
        assert section_record.model == the_section.model
        assert section_record.addition == the_section.addition
        assert section_record.role == convert2json(the_section.role)
        assert section_record.temperature == the_section.temperature
        assert section_record.create_at == the_section.create_at
        branch_record = logbase.exec(
            select(TableBranch).where(
                (TableBranch.id == 0) & (TableBranch.belonging == 0)
                )
            ).first()
        assert branch_record.id == the_branch.id
        assert branch_record.belonging == the_branch.belonging
        assert branch_record.iterations == convert2json_list(the_branch.iterations)
    
def test_chat_method_with_existed_branch(recorded_log):
    '''Test whether method can make chat record 
    with updating existed section and branch record properly.'''
    # Switch to specific section
    section, branch = recorded_log.switch_section(1)
    # Switch to specific branch
    branch = recorded_log.switch_branch(0)
    # Make chat record
    recorded_log.chat(model='test-model-change',
                     addition='This is for test change.',
                     role=Role(prompt='test-system',
                               input='test-user',
                               output='test-assistant'),
                     input='Test-Input',output='Test-Output',
                     temperature=0.6)
    # Set standard value
    the_section = Section(id=1,
                          type='chat',
                          model='test-model-change',
                          addition='This is for test change.',
                          role=Role(prompt='test-system',
                                    input='test-user',
                                    output='test-assistant'),
                          temperature=0.6,
                          create_at=recorded_log.section.create_at)
    the_branch = Branch(id=0,
                        belonging=1,
                        iterations=[
                            Iteration('Greeting!','Hi, How can I help you?'),
                            Iteration('Test-Input','Test-Output')])
    # Validate outcome
    assert section == recorded_log.section
    assert branch == recorded_log.branch
    assert section == the_section
    assert branch == the_branch
    assert recorded_log.section == the_section
    assert recorded_log.branch == the_branch
    with Session(recorded_log._engine) as logbase:
        section_record = logbase.exec(
            select(TableSection).where(TableSection.id == 1)
            ).first()
        assert section_record.id == the_section.id
        assert section_record.type == the_section.type
        assert section_record.model == the_section.model
        assert section_record.addition == the_section.addition
        assert section_record.role == convert2json(the_section.role)
        assert section_record.temperature == the_section.temperature
        assert section_record.create_at == the_section.create_at
        branch_record = logbase.exec(
            select(TableBranch).where(
                (TableBranch.id == 0) & (TableBranch.belonging == 1)
                )
            ).first()
        assert branch_record.id == the_branch.id
        assert branch_record.belonging == the_branch.belonging
        assert branch_record.iterations == convert2json_list(the_branch.iterations)

def test_chat_method_with_existed_section(recorded_log):
    '''Test whether method can make chat record 
    with updating existed section record properly.'''
    # Switch to specific section
    section, branch = recorded_log.switch_section(1)
    # Switch to specific branch
    recorded_log.switch_branch(0)
    # Create new branch
    branch = recorded_log.create_branch()
    # Make chat record
    recorded_log.chat(model='test-model-change',
                     addition='This is for test change.',
                     role=Role(prompt='test-system',
                               input='test-user',
                               output='test-assistant'),
                     input='Test-Input',output='Test-Output',
                     temperature=0.6)
    # Set standard value
    the_section = Section(id=1,
                          type='chat',
                          model='test-model-change',
                          addition='This is for test change.',
                          role=Role(prompt='test-system',
                                    input='test-user',
                                    output='test-assistant'),
                          temperature=0.6,
                          create_at=recorded_log.section.create_at)
    the_branch = Branch(id=1,
                        belonging=1,
                        iterations=[
                            Iteration('Greeting!','Hi, How can I help you?'),
                            Iteration('Test-Input','Test-Output')])
    # Validate outcome
    assert section == recorded_log.section
    assert branch == recorded_log.branch
    assert section == the_section
    assert branch == the_branch
    assert recorded_log.section == the_section
    assert recorded_log.branch == the_branch
    with Session(recorded_log._engine) as logbase:
        section_record = logbase.exec(
            select(TableSection).where(TableSection.id == 1)
            ).first()
        assert section_record.id == the_section.id
        assert section_record.type == the_section.type
        assert section_record.model == the_section.model
        assert section_record.addition == the_section.addition
        assert section_record.role == convert2json(the_section.role)
        assert section_record.temperature == the_section.temperature
        assert section_record.create_at == the_section.create_at
        branch_record = logbase.exec(
            select(TableBranch).where(
                (TableBranch.id == 1) & (TableBranch.belonging == 1)
                )
            ).first()
        assert branch_record.id == the_branch.id
        assert branch_record.belonging == the_branch.belonging
        assert branch_record.iterations == convert2json_list(the_branch.iterations)

def test_chat_method_with_call_section(recorded_log):
    '''Test whether method can raise exception properly
    when making chat record in call section record.'''
    # Switch to specific section
    recorded_log.switch_section(0)
    # Switch to specific branch
    recorded_log.switch_branch(0)
    # Make chat record
    with pytest.raises(LogInferenceTypeError,match='Inference type not compatible.'):
        recorded_log.chat(model='test-model',
                    addition='This is for test.',
                    role=Role(prompt='system',
                              input='user',
                              output='assistant'),
                              input='Test-Input',output='Test-Output',
                              temperature=0.6)
        
def test_chat_method_without_branch(recorded_log):
    '''Test whether method raise exception properly 
    when making chat record without specifiying the belonging branch.'''
    # Switch to specific section
    recorded_log.switch_section(1)
    # Make chat record
    with pytest.raises(LogBranchNotSetError,match='Branch has not been set.'):
        recorded_log.chat(model='test-model',
            addition='This is for test.',
            role=Role(prompt='system',
                        input='user',
                        output='assistant'),
                        input='Test-Input',output='Test-Output',
                        temperature=0.6)
        
def test_chat_method_without_section(loaded_log):
    '''Test whether method raise exception properly 
    when making chat record without specifiying the belonging section.'''
    # Make chat record    
    with pytest.raises(LogSectionNotSetError,match='Section has not been set.'):
        loaded_log.chat(model='test-model',
                        addition='This is for test.',
                        role=Role(prompt='system',
                                  input='user',
                                  output='assistant'),
                        input='Test-Input',output='Test-Output',
                        temperature=0.6)
        
## ============================== `get()` Method Test ============================== ##
def test_get_method(recorded_log):
    '''Test whether method can get specific log record properly.'''
    # Get log record
    record = recorded_log.get(1,0)
    # Set standard value
    the_record = Record(section=1,
                        type='chat',
                        model='test-model',
                        addition='This is for test.',
                        role=Role(prompt='system',
                                  input='user',
                                  output='assistant'),
                        branch=Branch(
                            id=0,
                            belonging=1,
                            iterations=[Iteration('Greeting!',
                                                  'Hi, How can I help you?')]
                            ),
                            temperature=0.7,
                            create_at=2345678.9)
    # Validate outcome
    assert record == the_record
    assert recorded_log.section == None
    assert recorded_log.branch == None

def test_get_method_with_not_existed_branch(recorded_log):
    '''Test whether method can raise exception properly 
    when getting not existed branch record of current section record.'''
    # Get log record
    with pytest.raises(LogBranchNotExistError,
                       match='Branch `1` not existed in Section `1`'):
        record = recorded_log.get(1,1)

def test_get_method_with_not_existed_section(recorded_log):
    '''Test whether method can raise exception properly 
    when getting not existed section record.'''
    with pytest.raises(LogSectionNotExistError,match='2'):
        record = recorded_log.get(2,0)