import pytest
from llyra.components import Prompt
from llyra.components.utils import Role, Iteration

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

@pytest.fixture
def iterated_prompt():
    iterated_prompt = Prompt()
    iterated_prompt._iteration.append({'role': 'user', 'content': 'Hello, there!'})
    iterated_prompt._iteration.append(
        {'role': 'assistant', 
         'content': 'Greeting, how can I assistant you today?'})
    return iterated_prompt

## =========================== `__init__()` Method Test =========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt._iteration == []

## ============================ `iterate()` Method Test ============================ ##
def test_iterate_method(prompt):
    '''Test whether the method can make iteration record properly.'''
    role = Role('system','user','assistant')
    # Execute iteration record
    prompt.iterate(role,
                   'Hello, there!',
                   'Greeting, how can I assistant you today?')
    # Validate record value
    assert prompt._iteration == [
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
    prompt._iteration.append({'role': 'user', 'content': 'Dummy former record.'})
    # Execute iteration record
    prompt.iterate(role,
                   'Hello, there!',
                   'Greeting, how can I assistant you today?')
    # Validate record value
    assert prompt._iteration == [
        {'role': 'user', 'content': 'Dummy former record.'},
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]

def test_iterate_method_ignoring_not_recording_record(prompt):
    '''
    Test whether the method can ignore not recording iteration record 
    and record recording iteration record at the same time properly.
    '''
    role = Role('system','user','assistant')
    # Execute iteration record
    prompt.iterate(role,None,'Dummy Record')
    # Validate record value
    assert prompt._iteration == [{'role': 'assistant', 'content': 'Dummy Record'}]
    # Clear former iteration
    prompt._iteration = []
    # Execute iteration record
    prompt.iterate(role,'Dummy Record',None)
    # Validate record value
    assert prompt._iteration == [{'role': 'user', 'content': 'Dummy Record'}]

## ============================ `reload()` Method Test ============================ ##
def test_reload_method(iterated_prompt):
    '''Test whether the method can reload extra iteration history properly.'''
    extra_history = [Iteration(query='Dummy former query.',
                               response='Dummy former response.')]
    role = Role('system','user','assistant')
    # Execute reload record
    iterated_prompt.reload(role,extra_history)
    # Validate record value
    assert iterated_prompt._iteration == [
        {'role': 'user', 'content': 'Dummy former query.'},
        {'role': 'assistant', 'content': 'Dummy former response.'}]
    
def test_reload_method_without_iteration_history(prompt):
    '''Test whether the method can reload extra iteration history properly 
    when iteration history attribute is empty.'''
    extra_history = [Iteration(query='Dummy former query.',
                               response='Dummy former response.')]
    role = Role('system','user','assistant')
    # Execute reload record
    prompt.reload(role,extra_history)
    # Validate record value
    assert prompt._iteration == [
        {'role': 'user', 'content': 'Dummy former query.'},
        {'role': 'assistant', 'content': 'Dummy former response.'}]

def test_reload_method_clear_iteration_history(iterated_prompt):
    '''Test whether the method can clear iteration history properly 
    when extra iteration history is empty.'''
    role = Role('system','user','assistant')
    # Execute reload record
    iterated_prompt.reload(role,[])
    # Validate record value
    assert iterated_prompt._iteration == []

## ============================= `call()` Method Test ============================= ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single call inference properly.'''
    output = prompt.call('Hello, there!')
    assert output == 'Hello, there!'
    assert prompt._iteration == []

def test_call_method_with_iteration(iterated_prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make prompt for single call inference without addition properly.
    '''
    output = iterated_prompt.call('Hello, there!')
    assert output == 'Hello, there!'
    assert iterated_prompt._iteration == [
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
    assert prompt._iteration == []

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
    assert prompt._iteration == []

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
    assert iterated_prompt._iteration == [
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
    assert iterated_prompt._iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]