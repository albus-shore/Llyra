import pytest
from llyra.components import Log
from llyra.components.logs.utils import Section, Branch
from llyra.components.logs.utils import convert_dataclasses2jsonlist, convert_dataclass2json
from llyra.errors.components.logs import LogBranchNotCreatedError, LogBranchNotSetError
from llyra.errors.components.logs import LogSectionNotCreatedError, LogSectionNotSetError
from llyra.errors.components.logs import LogInferenceModeError
from llyra.components.utils import Role, Iteration
from sqlmodel import SQLModel, Session, create_engine, select

@pytest.fixture
def log():
    engine = create_engine('sqlite://')
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    log = Log(session)
    return log   

@pytest.fixture
def ready_log():
    engine = create_engine('sqlite://')
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    ready_log = Log(session)
    ready_log.change_section(-1)
    ready_log.change_branch(-1)
    return ready_log

@pytest.fixture
def recored_log():
    engine = create_engine('sqlite://')
    SQLModel.metadata.create_all(engine)
    session = Session(engine)
    recored_log = Log(session)
    recored_log.change_section(-1)
    recored_log.change_branch(-1)
    recored_log.call(model='test_model',
                   input='Test_1!',output='Success_1!',
                   temperature=0.7)
    recored_log.change_section(-1)
    recored_log.change_branch(-1)  
    recored_log.chat(model='test_model',
                   addition='This is for test_2.',
                   role=Role(prompt='test_system_2',
                             input='test_user_2',
                             output='test_assistant_2'),
                   input='Test_2!',output='Success_2!',
                   temperature=0.5)
    return recored_log

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(log):
    '''Test whether the class can be initialized properly.'''
    assert log.section == None
    assert log.branch == None
    assert log.iterations == None

## ======================== `change_section()` Method Test ======================== ##
def test_change_section_method_creating_new_section(log):
    '''Test whether the method can create new section properly.'''
    # Execute section operation
    log.change_section(-1)
    # Validate execute outcome
    assert log.section == Section(id=0,create_at=log.section.create_at)
    assert log.branch == None
    assert log.iterations == None

def test_change_section_method_recalling_section(recored_log):
    '''Test whether the method can recall section properly.'''
    # Execute section operation
    recored_log.change_section(0)
    # Validate execute outcome
    assert recored_log.section == Section(id=0,type='call',
        model='test_model',
        addition=None,
        role=None,
        temperature=0.7,
        create_at=recored_log.section.create_at,
        branches=[Branch(id=0,
            belonging=0,
            iterations=convert_dataclasses2jsonlist([Iteration(query='Test_1!',
                                                               response='Success_1!')])
                            )
                    ]
        )
    assert recored_log.branch == None
    assert recored_log.iterations == None
    # Execute section operation
    recored_log.change_section(1)
    # Validate execute outcome
    assert recored_log.section == Section(id=1,type='chat',
        model='test_model',
        addition='This is for test_2.',
        role=convert_dataclass2json(Role(prompt='test_system_2',
                                         input='test_user_2',
                                         output='test_assistant_2')),
        temperature=0.5,
        create_at=recored_log.section.create_at,
        branches=[Branch(id=0,
            belonging=1,
            iterations=convert_dataclasses2jsonlist([Iteration(query='Test_2!',
                                                               response='Success_2!')])
                            )
                    ]
        )
    assert recored_log.branch == None
    assert recored_log.iterations == None

def test_change_section_method_out_of_section_range(recored_log):
    '''Test whether the method can raise expection properly
    when id is out of range.'''
    with pytest.raises(LogSectionNotCreatedError,match='2'):
        recored_log.change_section(2)

## ========================= `change_branch()` Method Test ========================= ##
def test_change_branch_method_creating_new_branch(log):
    '''Test whether the method can create new branch properly.'''
    # Execute branch operation
    log.change_section(-1)
    log.change_branch(-1)
    # Validate execute outcome
    assert log.section == Section(id=0,create_at=log.section.create_at)
    assert log.branch == Branch(id=0)
    assert log.iterations == []

def test_change_branch_method_recalling_branch(recored_log):
    '''Test whether the method can recall branch in the section properly.'''
    # Execute branch operation
    recored_log.change_branch(0)
    # Validate execute outcome
    assert recored_log.branch == Branch(id=0,
        belonging=1,
        iterations=convert_dataclasses2jsonlist([Iteration(query='Test_2!',
                                                           response='Success_2!')]))
    assert recored_log.iterations == [Iteration(query='Test_2!',
                                                response='Success_2!')]

def test_change_branch_method_out_of_branch_range(recored_log):
    '''Test whether the method can raise exception properly
    when id is out of range.'''
    # Execute section operation
    recored_log.change_section(1)
    # Execute branch outcome
    with pytest.raises(LogBranchNotCreatedError,
                       match="Branch `1` hasn't been created in Section `1`."):
        recored_log.change_branch(1)
    
def test_change_branch_method_not_setting_section(log):
    '''Test whether the method can raise exception properly
    when section is not set.'''
    with pytest.raises(LogSectionNotSetError,match="Section hasn't been set."):
        log.change_branch(-1)    

## ============================= `call()` Method Test ============================= ## 
def test_call_method(ready_log):
    '''Test whether the method can make call record properly.''' 
    # Execute record operation
    ready_log.call(model='test_model',
                   input='Test!',output='Success!',
                   temperature=0.7)      
    # Seek record outcome
    statement = select(Section).where(Section.id==0)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_iteration = Iteration(query='Test!',response='Success!')
    assert ready_log.iterations == [the_iteration]
    the_branch = Branch(id=0,belonging=0,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[0] == the_branch
    the_section = Section(id=0,type='call',
                          model='test_model',
                          addition=None,
                          role=None,
                          temperature=0.7,
                          create_at=section.create_at,
                          branches=[the_branch])
    assert section == the_section

def test_call_method_with_multiple_branch(ready_log):
    '''Test whether the method can make multiple call record properly 
    in multiple branches in one section.'''
    # Execute former record operation
    ready_log.call(model='test_model',
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)  
    # Create new branch
    ready_log.change_branch(-1)
    # Execute record operation
    ready_log.call(model='test_model',
                   input='Test-2!',output='Success-2!',
                   temperature=0.5)  
    # Seek record outcome
    statement = select(Section).where(Section.id==0)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_former_iteration = Iteration(query='Test-1!',response='Success-1!')
    the_iteration = Iteration(query='Test-2!',response='Success-2!')
    assert ready_log.iterations == [the_iteration]
    the_former_branch = Branch(id=0,belonging=0,
        iterations=convert_dataclasses2jsonlist([the_former_iteration]))
    assert section.branches[0] == the_former_branch
    the_branch = Branch(id=1,belonging=0,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[1] == the_branch
    the_section = Section(id=0,type='call',
                          model='test_model',
                          addition=None,
                          role=None,
                          temperature=0.5,
                          create_at=section.create_at,
                          branches=[the_former_branch,the_branch])
    assert section == the_section

def test_call_method_with_multiple_section(ready_log):
    '''Test whether the method can make multiple call record properly
    in one branches of multiple sections.'''
    # Execute former record operation
    ready_log.call(model='test_model_1',
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)  
    # Create new section
    ready_log.change_section(-1)
    ready_log.change_branch(-1)
    # Execute record operation
    ready_log.call(model='test_model_2',
                   input='Test-2!',output='Success-2!',
                   temperature=0.5)  
    # Seek record outcome
    former_statement = select(Section).where(Section.id==0)
    former_section = ready_log._logbase.exec(former_statement).one()
    statement = select(Section).where(Section.id==1)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_former_iteration = Iteration(query='Test-1!',response='Success-1!')
    the_iteration = Iteration(query='Test-2!',response='Success-2!')
    assert ready_log.iterations == [the_iteration]
    the_former_branch = Branch(id=0,belonging=0,
        iterations=convert_dataclasses2jsonlist([the_former_iteration]))
    assert former_section.branches[0] == the_former_branch
    the_former_section = Section(id=0,type='call',
                                 model='test_model_1',
                                 addition=None,
                                 role=None,temperature=0.7,
                                 create_at=former_section.create_at,
                                 branches=[the_former_branch])
    assert former_section == the_former_section
    the_branch = Branch(id=0,belonging=1,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[0] == the_branch
    the_section = Section(id=1,type='call',
                          model='test_model_2',
                          addition=None,
                          role=None,temperature=0.5,
                          create_at=section.create_at,
                          branches=[the_branch])
    assert section == the_section

def test_call_method_multiple_call_in_one_branch(ready_log):
    '''Test whether the method can raise exception properly
    when execute multiple call in one branch.'''
    # Execute former record operation
    ready_log.call(model='test_model',
                   input='Test!',output='Success!',
                   temperature=0.7)   
    # Execute record operation
    with pytest.raises(LogInferenceModeError,match="Inference mode not compatible."):
        ready_log.call(model='test_model',
                       input='Test!',output='Success!',
                       temperature=0.7)   
        
def test_call_method_with_error_type(ready_log):
    '''Test whether the method can raise exception properly 
    when execute call in wrong type section.'''
    # Set wrong type
    ready_log.section.type = 'chat'
    # Execute record operation
    with pytest.raises(LogInferenceModeError,match="Inference mode not compatible."):
        ready_log.call(model='test_model',
                       input='Test!',output='Success!',
                       temperature=0.7)   
        
def test_call_method_not_setting_branch(log):
    '''Test whether the method can raise exception properly
    when execute call without setting branch.'''
    log.change_section(-1)
    with pytest.raises(LogBranchNotSetError,match="Branch hasn't been set."):
        log.call(model='test_model',
                       input='Test!',output='Success!',
                       temperature=0.7) 
        
def test_call_method_not_setting_section(log):
    '''Test whether the method can raise exception properly 
    when execute call without setting section.'''
    with pytest.raises(LogSectionNotSetError,match="Section hasn't been set."):
        log.call(model='test_model',
                       input='Test!',output='Success!',
                       temperature=0.7) 
        
## ============================= `chat()` Method Test ============================= ##
def test_chat_method(ready_log):
    '''Test whether the method can make chat record properly.'''
    # Execute record operation
    ready_log.chat(model='test_model',
                   addition='This is for test.',
                   role=Role(prompt='test_system',
                             input='test_user',
                             output='test_assistant'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)
    # Seek record outcome
    statement = select(Section).where(Section.id==0)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_iteration = Iteration(query='Test-1!',response='Success-1!')
    assert ready_log.iterations == [the_iteration]
    the_branch = Branch(belonging=0,id=0,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[0] == the_branch
    the_section = Section(id=0,type='chat',model='test_model',
                          addition='This is for test.',
                          role='{"prompt": "test_system", "input": "test_user", "output": "test_assistant"}',
                          temperature=0.7,
                          create_at=section.create_at,
                          branches=[the_branch])
    assert section == the_section
    
def test_chat_method_with_multiple_iteration(ready_log):
    '''Test whether the method can make multiple chat iteration properly 
    in one branch.'''
    # Execute former record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_1.',
                   role=Role(prompt='test_system_1',
                             input='test_user_1',
                             output='test_assistant_1'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)
    # Execute record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_2.',
                   role=Role(prompt='test_system_2',
                             input='test_user_2',
                             output='test_assistant_2'),
                   input='Test-2!',output='Success-2!',
                   temperature=0.5)
    # Seek record outcome
    statement = select(Section).where(Section.id==0)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_former_iteration = Iteration(query='Test-1!',response='Success-1!')
    the_iteration = Iteration(query='Test-2!',response='Success-2!')
    assert ready_log.iterations == [the_former_iteration,the_iteration]
    the_branch = Branch(belonging=0,id=0,
        iterations=convert_dataclasses2jsonlist([the_former_iteration, the_iteration]))
    assert section.branches[0] == the_branch
    the_section = Section(id=0,type='chat',model='test_model',
                          addition='This is for test_2.',
                          role=convert_dataclass2json(Role(prompt='test_system_2',
                                                           input='test_user_2',
                                                           output='test_assistant_2')),
                          temperature=0.5,
                          create_at=section.create_at,
                          branches=[the_branch])
    assert section == the_section

def test_chat_method_with_multiple_branch(ready_log):
    '''Test whether the method can make multiple chat iterations properly 
    in multiple branches in one section.'''
    # Execute former record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_1.',
                   role=Role(prompt='test_system_1',
                             input='test_user_1',
                             output='test_assistant_1'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)
    # Create new branch
    ready_log.change_branch(-1)
    # Execute record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_2.',
                   role=Role(prompt='test_system_2',
                             input='test_user_2',
                             output='test_assistant_2'),
                   input='Test-2!',output='Success-2!',
                   temperature=0.5)
    # Seek record outcome
    statement = select(Section).where(Section.id==0)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_former_iteration = Iteration(
        query='Test-1!',response='Success-1!')
    the_iteration = Iteration(query='Test-2!',response='Success-2!')
    assert ready_log.iterations == [the_iteration]
    the_former_branch = Branch(belonging=0,id=0,
        iterations=convert_dataclasses2jsonlist([the_former_iteration]))
    assert section.branches[0] == the_former_branch
    the_branch = Branch(belonging=0,id=1,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[1] == the_branch
    the_section = Section(id=0,type='chat',model='test_model',
                          addition='This is for test_2.',
                          role=convert_dataclass2json(Role(prompt='test_system_2',
                                                           input='test_user_2',
                                                           output='test_assistant_2')),
                          temperature=0.5,
                          create_at=section.create_at,
                          branches=[the_former_branch, the_branch])
    assert section == the_section

def test_chat_method_with_multiple_section(ready_log):
    '''Test whether the method can make multiple chat iterations properly
    in one branches of multiple sections.'''
    # Execute former record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_1.',
                   role=Role(prompt='test_system_1',
                             input='test_user_1',
                             output='test_assistant_1'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)
    # Create new section
    ready_log.change_section(-1)
    ready_log.change_branch(-1)    
    # Execute record operation
    ready_log.chat(model='test_model',
                   addition='This is for test_2.',
                   role=Role(prompt='test_system_2',
                             input='test_user_2',
                             output='test_assistant_2'),
                   input='Test-2!',output='Success-2!',
                   temperature=0.5)
    # Seek record outcome
    former_statement = select(Section).where(Section.id==0)
    former_section = ready_log._logbase.exec(former_statement).one()
    statement = select(Section).where(Section.id==1)
    section = ready_log._logbase.exec(statement).one()
    # Validate record value
    the_former_iteration = Iteration(query='Test-1!',response='Success-1!')
    the_iteration = Iteration(query='Test-2!',response='Success-2!')
    assert ready_log.iterations == [the_iteration]
    the_former_branch = Branch(belonging=0,id=0,
        iterations=convert_dataclasses2jsonlist([the_former_iteration]))
    assert former_section.branches[0] == the_former_branch
    the_branch = Branch(belonging=1,id=0,
        iterations=convert_dataclasses2jsonlist([the_iteration]))
    assert section.branches[0] == the_branch
    the_former_section = Section(id=0,type='chat',model='test_model',
                          addition='This is for test_1.',
                          role=convert_dataclass2json(Role(prompt='test_system_1',
                                                           input='test_user_1',
                                                           output='test_assistant_1')),
                          temperature=0.7,
                          branches=[the_former_branch],
                          create_at=former_section.create_at,)
    assert former_section == the_former_section
    the_section = Section(id=1,type='chat',model='test_model',
                          addition='This is for test_2.',
                          role=convert_dataclass2json(Role(prompt='test_system_2',
                                                           input='test_user_2',
                                                           output='test_assistant_2')),
                          temperature=0.5,
                          branches=[the_branch],
                          create_at=section.create_at,)
    assert section == the_section

def test_chat_method_with_error_type(recored_log):
    '''Test whether the method can raise exception properly 
    when execute chat in wrong type section.'''
    # Set wrong type
    recored_log.change_section(0)
    recored_log.change_branch(0)
    # Execute record operation
    with pytest.raises(LogInferenceModeError,match="Inference mode not compatible."):
        recored_log.chat(model='test_model',
                   addition='This is for test.',
                   role=Role(prompt='test_system',
                             input='test_user',
                             output='test_assistant'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7) 
        
def test_chat_method_not_setting_branch(log):
    '''Test whether the method can raise exception properly
    when execute chat without setting branch.'''
    log.change_section(-1)
    with pytest.raises(LogBranchNotSetError,match="Branch hasn't been set."):
        log.chat(model='test_model',
                   addition='This is for test.',
                   role=Role(prompt='test_system',
                             input='test_user',
                             output='test_assistant'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7)
        
def test_chat_method_not_setting_section(log):
    '''Test whether the method can raise exception properly 
    when execute chat without setting section.'''
    with pytest.raises(LogSectionNotSetError,match="Section hasn't been set."):
        log.chat(model='test_model',
                   addition='This is for test.',
                   role=Role(prompt='test_system',
                             input='test_user',
                             output='test_assistant'),
                   input='Test-1!',output='Success-1!',
                   temperature=0.7) 

## ============================== `get()` Method Test ============================== ##
def test_get_method(recored_log):
    '''Test whether the method can get specific branch in specific section properly.'''
    record_1 = recored_log.get(0,0)
    the_record_1 = {'id': 0,
                  'type': 'call',
                  'model': 'test_model',
                  'addition': None,
                  'role': None,
                  'temperature': 0.7,
                  'create_at': record_1['create_at'],
                  'branch': {'id': 0,
                                'belonging': 0,
                                'iterations': [{'query': 'Test_1!',
                                                'response': 'Success_1!'}]}}
    assert record_1 == the_record_1
    record_2 = recored_log.get(1,0)
    the_record_2 = {'id': 1,
                  'type': 'chat',
                  'model': 'test_model',
                  'addition': 'This is for test_2.',
                  'role': {'prompt': 'test_system_2',
                           'input': 'test_user_2',
                           'output': 'test_assistant_2'},
                  'temperature': 0.5,
                  'create_at': record_2['create_at'],
                  'branch': {'id': 0,
                                'belonging': 1,
                                'iterations': [{'query': 'Test_2!',
                                                'response': 'Success_2!'}]}}
    assert record_2 == the_record_2

def test_get_method_out_of_branch_range(recored_log):
    '''Test whether the method can raise exception properly 
    when branch id is out of range.'''
    with pytest.raises(LogBranchNotCreatedError,
                       match="Branch `1` hasn't been created in Section `1`."):
        recored_log.get(1,1)

def test_get_method_out_of_section_range(recored_log):
    '''Test whether the method can raise exception properly 
    when section id is out of range.'''
    with pytest.raises(LogSectionNotCreatedError,match='2'):
        recored_log.get(2,0)

def test_get_method_invalid(recored_log):
    '''Test whether the method can raise exception properly
    when input is invalid.'''
    with pytest.raises(ValueError,match='Invalid input.'):
        recored_log.get(-1,0)
    with pytest.raises(ValueError,match='Invalid input.'):
        recored_log.get(0,-1)
    with pytest.raises(ValueError,match='Invalid input.'):
        recored_log.get(-1,-1)