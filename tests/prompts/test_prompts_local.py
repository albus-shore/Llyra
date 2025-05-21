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



