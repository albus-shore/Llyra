import pytest
from llyra.remote.prompts import PromptRemote

@pytest.fixture
def prompt():
    prompt = PromptRemote()
    return prompt

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference prrperly.'''
    output = prompt.call('Evening!')
    assert output == 'Evening!'
    assert prompt._iteration == []
