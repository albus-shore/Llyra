import pytest
from llyra.local.prompts import Prompt

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

## ========================== Initialize Method Test ========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt.iteration == []

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference prrperly.'''
    output = prompt.call({'input': '<|User|>', 'output': '<|Assistant|>'},
                         'Evening!')
    assert output == '<|User|>Evening!<|Assistant|>'
    assert prompt.iteration == []

def test_chat_method_without_iteration(prompt):
    '''Test whether the method can make prompt for iterative chat inference properly.'''
    role = {
        "prompt": "system",
        "input": "user",
        "output": "assistant"
        }
    content = 'hello,there!'
    addition = 'This is for test.'
    output = prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'system': 'This is for test.'},
        {'user': 'hello,there!'}
        ]
    assert prompt.iteration == []
    output = prompt.chat(role=role,content=content,addition=None)
    assert output == [
        {'user': 'hello,there!'}
        ]
    assert prompt.iteration == []

def test_chat_method_with_iteration(prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make promp for iterative chat inference properly.
    '''
    prompt.iteration.append({'user': 'Hello, there!'})
    prompt.iteration.append({'assistant': 'Greeting, how can I assistant you today?'})
    role = {
        "prompt": "system",
        "input": "user",
        "output": "assistant"
        }
    content = 'hello,there!'
    addition = 'This is for test.'
    output = prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'user': 'Hello, there!'},
        {'assistant': 'Greeting, how can I assistant you today?'},
        {'system': 'This is for test.'},
        {'user': 'hello,there!'}
        ]
    assert prompt.iteration == [
        {'user': 'Hello, there!'},
        {'assistant': 'Greeting, how can I assistant you today?'},
        ]

## =========================== Iterate Method Test =========================== ##
def test_iterate_method(prompt):
    '''Teset whether the method can make iteration record properly.'''
    prompt.iterate('user','Hello, there!',True)
    assert prompt.iteration == [{'user': 'Hello, there!'}]
    prompt.iterate('assistant','Greeting, how can I assistant you today?',True)
    assert prompt.iteration == [
        {'user': 'Hello, there!'},
        {'assistant': 'Greeting, how can I assistant you today?'}
        ]
    prompt.iterate('user','Introduce yourself.',False)
    assert prompt.iteration == [{'user': 'Introduce yourself.'}]
    prompt.iterate(None,'This is for test.',True)
    assert prompt.iteration == [{'user': 'Introduce yourself.'}]
    prompt.iterate('user',None,True)
    assert prompt.iteration == [{'user': 'Introduce yourself.'}]
    prompt.iterate(None,None,True)
    assert prompt.iteration == [{'user': 'Introduce yourself.'}]
    prompt.iterate(None,None,False)
    assert prompt.iteration == []