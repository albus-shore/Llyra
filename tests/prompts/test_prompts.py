import pytest
from llyra.local.prompts import Prompt

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

## ========================== Initialize Method Test ========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference prrperly.'''
    output = prompt.call({'input': '<|User|>', 'output': '<|Assistant|>'},
                         'Evening!')
    assert output == '<|User|>Evening!<|Assistant|>'
