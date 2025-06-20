import pytest
from llyra.components import Prompt
from llyra.components.utils import Role

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

@pytest.fixture
def iterated_prompt():
    iterated_prompt = Prompt()
    iterated_prompt.iteration.append({'role': 'user', 'content': 'Hello, there!'})
    iterated_prompt.iteration.append(
        {'role': 'assistant', 
         'content': 'Greeting, how can I assistant you today?'})
    return iterated_prompt

## =========================== `__init__()` Method Test =========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt.iteration == []

## ============================ `iterate()` Method Test ============================ ##
def test_iterate_method(prompt):
    '''Test whether the method can make iteration record properly.'''
    role = Role('system','user','assistant')
    # Execute iteration record
    prompt.iterate(role,
                   'Hello, there!',
                   'Greeting, how can I assistant you today?',
                   True)
    # Validate record value
    assert prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]

def test_iterate_method_keeping_recording(prompt):
    '''
    Test whether the method can make iteration record 
    with former iteration record properly.
    '''
    role = Role('system','user','assistant')
    # Set former executive value
    prompt.iteration.append({'role': 'user', 'content': 'Dummy former record.'})
    # Execute iteration record
    prompt.iterate(role,
                   'Hello, there!',
                   'Greeting, how can I assistant you today?',
                   True)
    # Validate record value
    assert prompt.iteration == [
        {'role': 'user', 'content': 'Dummy former record.'},
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]
    
def test_iterate_method_starting_new_record(prompt):
    '''Test whether the method can make new iteration record properly.'''
    role = Role('system','user','assistant')
    # Set former executive value
    prompt.iteration.append({'role': 'user', 'content': 'Hello, there!'})
    # Execute iteration record
    prompt.iterate(role,
                   'Introduce yourself.',
                   'Greeting, how can I assistant you today?',
                   False)
    # Validate record value
    assert prompt.iteration == [
        {'role': 'user', 'content': 'Introduce yourself.'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]

def test_iterate_method_ignoring_invalid_record(prompt):
    '''Test whether the method can ignore invalid iteration record properly.'''
    # Execute iteration record
    prompt.iterate(None,'This is for test.','Dummy Record',True)
    # Validate record value
    assert prompt.iteration == []

def test_iterate_method_ignoring_not_recording_record(prompt):
    '''
    Test whether the method can ignore not recording iteration record 
    and record recording iteration record at the same time properly.
    '''
    role = Role('system','user','assistant')
    # Execute iteration record
    prompt.iterate(role,None,'Dummy Record',True)
    # Validate record value
    assert prompt.iteration == [{'role': 'assistant', 'content': 'Dummy Record'}]
    # Clear former iteration
    prompt.iteration = []
    # Execute iteration record
    prompt.iterate(role,'Dummy Record',None,True)
    # Validate record value
    assert prompt.iteration == [{'role': 'user', 'content': 'Dummy Record'}]

## ============================= `call()` Method Test ============================= ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single call inference properly.'''
    output = prompt.call('Hello, there!')
    assert output == 'Hello, there!'
    assert prompt.iteration == []

def test_call_method_with_iteration(iterated_prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make prompt for single call inference without addition properly.
    '''
    output = iterated_prompt.call('Hello, there!')
    assert output == 'Hello, there!'
    assert iterated_prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]


## ============================= `chat()` Method Test ============================= ##
def test_chat_method_without_iteration_and_addition(prompt):
    '''
    Test whether the method can make prompt for iterative chat inference 
    without iteration and addition properly.
    '''
    role = Role('system','user','assistant')
    content = 'hello,there!'
    output = prompt.chat(role=role,content=content,addition=None)
    assert output == [
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt.iteration == []

def test_chat_method_without_iteration_and_with_addition(prompt):
    '''
    Test whether the method can make prompt for iterative chat inference 
    without iteration and with addition properly.
    '''
    role = Role('system','user','assistant')
    content = 'hello,there!'
    addition = 'This is for test.'
    output = prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'role': 'system','content': 'This is for test.'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt.iteration == []

def test_chat_method_with_iteration_and_without_addition(iterated_prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make prompt for iterative chat inference without addition properly.
    '''
    role = Role('system','user','assistant')
    content = 'hello,there!'
    output = iterated_prompt.chat(role=role,content=content,addition=None)
    assert output == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 
         'content': 'Greeting, how can I assistant you today?'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert iterated_prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]

def test_chat_method_with_iteration_and_addition(iterated_prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make prompt for iterative chat inference with addition properly.
    '''
    role = Role('system','user','assistant')
    content = 'hello,there!'
    addition = 'This is for test.'
    output = iterated_prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'role': 'system', 'content': 'This is for test.'},
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 
         'content': 'Greeting, how can I assistant you today?'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert iterated_prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]