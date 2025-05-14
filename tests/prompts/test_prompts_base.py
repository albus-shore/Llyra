import pytest
from llyra.base.prompts import Prompt

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

## ========================== Initialize Method Test ========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt._iteration == []

## =========================== Iterate Method Test =========================== ##
def test_iterate_method(prompt):
    '''Teset whether the method can make iteration record properly.'''
    prompt.iterate('user','Hello, there!',True)
    assert prompt._iteration == [{'role': 'user', 'content': 'Hello, there!'}]
    prompt.iterate('assistant','Greeting, how can I assistant you today?',True)
    assert prompt._iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]
    prompt.iterate('user','Introduce yourself.',False)
    assert prompt._iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,'This is for test.',True)
    assert prompt._iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate('user',None,True)
    assert prompt._iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,None,True)
    assert prompt._iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,None,False)
    assert prompt._iteration == []    