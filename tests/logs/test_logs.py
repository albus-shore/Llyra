import pytest
from llyra.components import Log
from llyra.components.logs.utils import Section, make_new_iteration
from llyra.components.utils import Role

@pytest.fixture
def log():
    log = Log()
    return log

@pytest.fixture
def recorded_log():
    recorded_log = Log()
    # Set first log record
    recorded_log.call(model='model',
             input='hello, there!',
             output='hello, how can I assist you today?',
             temperature=0.6)
    # Set second log record
    ## Set executive value
    addition = 'This is for test.'
    role = Role('system','user','assistant')
    ## Execute iterative chat log record
    recorded_log.chat(model='model',
             addition=addition,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             keep=True)
    # Set third log record
    recorded_log.call(model='model',
             input='Greeting, there!',
             output='hello, how can I assist you today?',
             temperature=0.6)
    # Return recorded log
    return recorded_log
    

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(log):
    '''Test whether the class can be initialized properly.'''
    assert log.id == 0
    assert log._history == []

## ============================= `call()` Method Test ============================= ##
def test_call_method(log):
    '''Test whether the method can record inference history properly.'''
    # Execute single call log record
    log.call(model='model',
             input='hello, there!',
             output='hello, how can I assist you today?',
             temperature=0.6)
    # Set stardard value
    iteration = make_new_iteration('hello, there!',
                                   'hello, how can I assist you today?')
    section = Section(0,'call','model',None,None,0.6)
    section.create_at = log._history[0].create_at
    section.iteration.append(iteration)
    # Validate record value
    assert log.id == 1
    assert log._history == [section]
    
## ============================= `chat()` method test ============================= ##    
def test_chat_method(log):
    '''Test whether the method can record inference history properly.'''
    # Set executive value
    addition = 'This is for test.'
    role = Role('system','user','assistant')
    # Execute iterative chat log record
    log.chat(model='model',
             addition=addition,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             keep=True)
    # Set stardard value
    iteration = make_new_iteration('Hello, there!',
                                   'Greeting, how can I assist you today?')
    section = Section(0,'chat','model',addition,role,0.6)
    section.create_at = log._history[0].create_at
    section.iteration.append(iteration)
    # Validate record value
    assert log.id == 1
    assert log._history == [section]

def test_chat_method_keeping_recording(log):
    '''Test whether the method can keep recording inference history properly.'''
    # Set executive value
    addition = 'This is for test.'
    role = Role('system','user','assistant')
    # Set former executive value
    iteration = make_new_iteration('Hello, there!',
                                   'Greeting, how can I assist you today?')
    section = Section(0,'chat','model',addition,role,0.6)
    section.create_at = 0
    section.iteration.append(iteration)
    log._history.append(section)
    log.id += 1
    # Execute iterative chat log record
    log.chat(model='model',
             addition=addition,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             keep=True)
    # Set stardard value
    iteration = make_new_iteration('Good day!',
                                   'Greeting, how can I assist you today?')
    section.iteration.append(iteration)
    # Validate record value
    assert log.id == 1
    assert log._history == [section]

def test_chat_method_not_keeping_recording_manually(log):
    '''Test whether the method can stop keeping recording inference history properly
    when `keep` is set to `False`.'''
    # Set executive value
    addition = 'This is for test.'
    role = Role('system','user','assistant')
    # Set former executive value
    iteration = make_new_iteration('Hello, there!',
                                   'Greeting, how can I assist you today?')
    former_section = Section(0,'chat','model',addition,role,0.6)
    former_section.create_at = 0
    former_section.iteration.append(iteration)
    log._history.append(former_section)
    log.id += 1
    # Execute iterative chat log record
    log.chat(model='model',
             addition=addition,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             keep=False)
    # Set stardard value
    iteration = make_new_iteration('Good day!',
                                   'Greeting, how can I assist you today?')
    section = Section(1,'chat','model',addition,role,0.6)
    section.create_at = log._history[1].create_at
    section.iteration.append(iteration)
    # Validate record value
    assert log.id == 2
    assert log._history == [former_section,section]

def test_chat_method_not_keeping_recording_automatically(log):
    '''Test whether the method can stop keeping recording inference history properly
    when `keep` is set to `False` but last iteration is `call`.'''
    # Set former executive value
    iteration = make_new_iteration('hello, there!',
                                   'hello, how can I assist you today?')
    former_section = Section(0,'call','model',None,None,0.6)
    former_section.create_at = 0
    former_section.iteration.append(iteration)
    log._history.append(former_section)
    log.id += 1
    # Set executive value
    addition = 'This is for test.'
    role = Role('system','user','assistant')
    # Execute iterative chat log record
    log.chat(model='model',
             addition=addition,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             keep=True)
    # Set stardard value
    iteration = make_new_iteration('Hello, there!',
                                   'Greeting, how can I assist you today?')
    section = Section(1,'chat','model',addition,role,0.6)
    section.create_at = log._history[1].create_at
    section.iteration.append(iteration)
    # Validate record value
    assert log.id == 2
    assert log._history == [former_section,section]

## ============================== `get()` method test ============================== ##
def test_get_method_with_specific_id(recorded_log):
    '''Test wether the method return readable log with provided id properly.'''
    the_log = recorded_log.get(1)
    assert recorded_log.id == 3
    assert the_log == {
        'id': 1,
        'type': 'chat',
        'model': 'model',
        'addition': 'This is for test.',
        'role': {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant',
            },
        'temperature': 0.6,
        'create_at': the_log['create_at'],
        'iteration': [{'query':'Hello, there!',
                       'response':'Greeting, how can I assist you today?'}],
        }
    
def test_get_method_for_all_logs(recorded_log):
    '''Test wether the method return a list of all readable log properly.'''
    the_log = recorded_log.get(-1)
    assert recorded_log.id == 3
    assert the_log == [
        {
        'id':0,
        'type':'call',
        'model':'model',
        'addition':None,
        'role':None,
        'temperature': 0.6,
        'create_at': recorded_log._history[0].create_at,
        'iteration':[{'query':'hello, there!',
                      'response':'hello, how can I assist you today?'}],
        },{
        'id': 1,
        'type': 'chat',
        'model': 'model',
        'addition': 'This is for test.',
        'role': {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant',
            },
        'temperature': 0.6,
        'create_at': recorded_log._history[1].create_at,
        'iteration': [{'query':'Hello, there!',
                       'response':'Greeting, how can I assist you today?'}],
        },{
        'id':2,
        'type':'call',
        'model':'model',
        'addition':None,
        'role':None,
        'temperature': 0.6,
        'create_at': recorded_log._history[2].create_at,    
        'iteration': [{'query':'Greeting, there!',
                       'response':'hello, how can I assist you today?'}],
        }]
    
def test_get_method_with_invalid_id(log):
    '''Test wether the method raise exception properly when meeting invalid id.'''
    with pytest.raises(IndexError,match='Error: Record not created.'):
        log.get(1)