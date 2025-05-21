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

## ========================== Generate Methods Test ========================== ##
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
        {'role': 'system','content': 'This is for test.'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt._iteration == []
    output = prompt.chat(role=role,content=content,addition=None)
    assert output == [
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt._iteration == []

def test_chat_method_with_iteration(prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make promp for iterative chat inference properly.
    '''
    prompt._iteration.append({'role': 'user', 'content': 'Hello, there!'})
    prompt._iteration.append({'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'})
    role = {
        "prompt": "system",
        "input": "user",
        "output": "assistant"
        }
    content = 'hello,there!'
    addition = 'This is for test.'
    output = prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'role': 'system', 'content': 'This is for test.'},
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt._iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]