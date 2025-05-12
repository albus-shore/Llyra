import pytest
from llyra.remote.strategys import StrategyRemote

@pytest.fixture
def strategy():
    strategy = StrategyRemote()
    return strategy

### ============================== Initialize Test ============================== ###
def test_class_initialize(strategy):
    '''Test whether the class can be initialized properly.'''
    assert strategy.call.stop == None
    assert strategy.call.temperature == None
    assert strategy.chat.prompt == None
    assert strategy.chat.role == {
        'prompt': None,
        'input': None,
        'output': None,    
        }
    assert strategy.chat.stop == None
    assert strategy.chat.temperature == None

### ============================= Load Method Test ============================= ###
def test_load_strategy_file(strategy):
    '''Test whether method load strategy file form path properly.'''
    strategy.load('tests/strategys/strategy_remote.json')
    assert strategy.call.stop == '<EOF>'
    assert strategy.call.temperature == 0.6
    assert strategy.chat.prompt == 'This is used for test.'
    assert strategy.chat.role == {
        'prompt': "system",
        'input': "user",
        'output': "assistant",    
        }
    assert strategy.chat.stop == '<EOF>'
    assert strategy.chat.temperature == 0.6

### ============================ Update Method Test ============================ ###
## ========================== Update Call Strategy ========================== ##
def test_update_call_strategy(strategy):
    '''Test whether method update call strategy properly.'''
    strategy.update_call(stop='user',temperature=1)
    assert strategy.call.stop == 'user'
    assert strategy.call.temperature == 1

## ========================== Update Chat Strategy ========================== ##
def test_update_chat_strategy(strategy):
    '''Test whether method update chat strategy properly.'''
    strategy.update_chat(prompt='You are a kind assistant.',
                  prompt_role='system',input_role='user',output_role='assistant',
                  stop='<|end_of_sentence|>',temperature=1)
    assert strategy.chat.prompt == 'You are a kind assistant.'
    assert strategy.chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant',    
        }
    assert strategy.chat.stop == '<|end_of_sentence|>'
    assert strategy.chat.temperature == 1             