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
        {'role': 'system','content': 'This is for test.'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt.iteration == []
    output = prompt.chat(role=role,content=content,addition=None)
    assert output == [
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt.iteration == []

def test_chat_method_with_iteration(prompt):
    '''
    Test whether the method can not affect the iteration history.
    And make promp for iterative chat inference properly.
    '''
    prompt.iteration.append({'role': 'user', 'content': 'Hello, there!'})
    prompt.iteration.append({'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'})
    role = {
        "prompt": "system",
        "input": "user",
        "output": "assistant"
        }
    content = 'hello,there!'
    addition = 'This is for test.'
    output = prompt.chat(role=role,content=content,addition=addition)
    assert output == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        {'role': 'system', 'content': 'This is for test.'},
        {'role': 'user', 'content': 'hello,there!'}
        ]
    assert prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'},
        ]

## =========================== Iterate Method Test =========================== ##
def test_iterate_method(prompt):
    '''Teset whether the method can make iteration record properly.'''
    prompt.iterate('user','Hello, there!',True)
    assert prompt.iteration == [{'role': 'user', 'content': 'Hello, there!'}]
    prompt.iterate('assistant','Greeting, how can I assistant you today?',True)
    assert prompt.iteration == [
        {'role': 'user', 'content': 'Hello, there!'},
        {'role': 'assistant', 'content': 'Greeting, how can I assistant you today?'}
        ]
    prompt.iterate('user','Introduce yourself.',False)
    assert prompt.iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,'This is for test.',True)
    assert prompt.iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate('user',None,True)
    assert prompt.iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,None,True)
    assert prompt.iteration == [{'role': 'user', 'content': 'Introduce yourself.'}]
    prompt.iterate(None,None,False)
    assert prompt.iteration == []