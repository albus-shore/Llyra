import pytest
from llyra.local.prompts import PromptLocal

@pytest.fixture
def prompt():
    prompt = PromptLocal()
    return prompt

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference prrperly.'''
    output = prompt.call({'input': '<|User|>', 'output': '<|Assistant|>'},
                         'Evening!')
    assert output == '<|User|>Evening!<|Assistant|>'
    assert prompt._iteration == []

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

