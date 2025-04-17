import pytest
from llyra.local.prompts import Prompt

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

## ========================== Initialize Method Test ========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt.call_input == None
    assert prompt.call_output == None

## =========================== Config Method Test =========================== ##
def test_config_method(prompt):
    '''Test whether the method can set prompt config parameters properly.'''
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'})
    assert prompt.begin == '<|begin_of_sentence|>'
    assert prompt.end == '<|end_of_sentence|>'

## ============================= Set Method Test ============================= ##
def test_load_method(prompt):
    '''Test whether the method can set prompt parameter attributes properly.'''
    prompt.set({'input':'user','output':'assistant'})
    assert prompt.call_input == 'user'
    assert prompt.call_output == 'assistant'

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference prrperly.'''
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'})
    prompt.set({'input':'<|User|>','output':'<|Assistant|>'})
    output = prompt.call('Evening!')
    assert output == '<|begin_of_sentence|><|User|>Evening!<|Assistant|><|end_of_sentence|>'
