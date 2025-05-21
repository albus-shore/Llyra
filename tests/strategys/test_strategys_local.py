import pytest
from llyra.local.strategys import StrategyLocal

@pytest.fixture
def strategy():
    strategy = StrategyLocal()
    return strategy

### ============================== Initialize Test ============================== ###
def test_class_initialize(strategy):
    '''Test whether the class can be initialized properly.'''
    assert strategy.call.role == {
        'input': None,
        'output': None
        }
    assert strategy.call.stop == None
    assert strategy.call.tokens == None
    assert strategy.call.temperature == None
    assert strategy.chat.prompt == None
    assert strategy.chat.role == {
        'prompt': None,
        'input': None,
        'output': None
        }
    assert strategy.chat.stop == None
    assert strategy.chat.tokens == None
    assert strategy.chat.temperature == None

### ============================= Load Method Test ============================= ###
def test_load_strategy_file(strategy):
    '''Test whether method load strategy file form path properly.'''
    strategy.load('tests/strategys/strategy_local.json')
    assert strategy.call.role == {
        'input': "<|User|>",
        'output': "<|Assistant|>"
        }
    assert strategy.call.stop == "<|User|>"
    assert strategy.call.tokens == 128e3
    assert strategy.call.temperature == 0.6
    assert strategy.chat.prompt == 'This is used for test.'
    assert strategy.chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.chat.stop == '<|User|>'
    assert strategy.chat.tokens == 128e3
    assert strategy.chat.temperature == 0.6

## ========================== Load Call Strategy ========================== ##
def test_load_strategy_with_no_call_input_role(strategy):
    '''
    Test whether method show warning with no input role for call.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing input role parameter for call inference.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_input_role.json')
        assert strategy.call.role == {
            'input': None,
            'output': "<|Assistant|>"
            }
        assert strategy.call.stop == "<|User|>"
        assert strategy.call.tokens == 128e3
        assert strategy.call.temperature == 0.6

def test_load_strategy_with_no_call_output_role(strategy):
    '''
    Test whether method show warning with no output role for call.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing output role parameter for call inference.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_output_role.json')
        assert strategy.call.role == {
            'input': "<|User|>",
            'output': None
            }
        assert strategy.call.stop == "<|User|>"
        assert strategy.call.tokens == 128e3
        assert strategy.call.temperature == 0.6

def test_load_strategy_with_no_call_max_token(strategy):
    '''
    Test whether method show warning with no max_token.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_max_token.json')
        assert strategy.call.role == {
            'input': "<|User|>",
            'output': "<|Assistant|>"
            }
        assert strategy.call.stop == "<|User|>"
        assert strategy.call.tokens == None
        assert strategy.call.temperature == 0.6

def test_load_strategy_with_call_no_stop(strategy):
    '''
    Test whether method show warning with no stop.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_stop.json')
        assert strategy.call.role == {
            'input': "<|User|>",
            'output': "<|Assistant|>"
            }
        assert strategy.call.stop == None
        assert strategy.call.tokens == 128e3
        assert strategy.call.temperature == 0.6

def test_load_strategy_with_no_call_temperature(strategy):
    '''Test whether method load call strategy witout temperature from path properly.'''
    strategy.load('tests/strategys/strategy_no_call_temperature.json')
    assert strategy.call.role == {
        'input': "<|User|>",
        'output': "<|Assistant|>"
        }
    assert strategy.call.stop == "<|User|>"
    assert strategy.call.tokens == 128e3
    assert strategy.call.temperature == 0

## ========================== Load Chat Strategy ========================== ##
def test_load_strategy_with_no_chat_max_token(strategy):
    '''
    Test whether method show warning with no max_token.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_chat_max_token.json')
        assert strategy.chat.prompt == 'This is used for test.'
        assert strategy.chat.role == {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant'
            }
        assert strategy.chat.stop == '<|User|>'
        assert strategy.chat.tokens == None
        assert strategy.chat.temperature == 0.6

def test_load_strategy_with_no_chat_stop(strategy):
    '''
    Test whether method show warning with no stop.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_chat_stop.json')
        assert strategy.chat.prompt == 'This is used for test.'
        assert strategy.chat.role == {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant'
            }
        assert strategy.chat.stop == None
        assert strategy.chat.tokens == 128e3
        assert strategy.chat.temperature == 0.6

def test_load_strategy_with_no_chat_temperature(strategy):
    '''Test whether method load call strategy witout temperature from path properly.'''
    strategy.load('tests/strategys/strategy_no_chat_temperature.json')
    assert strategy.chat.prompt == 'This is used for test.'
    assert strategy.chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.chat.stop == '<|User|>'
    assert strategy.chat.tokens == 128e3
    assert strategy.chat.temperature == 0


### ============================ Update Method Test ============================ ###
## ========================== Update Call Strategy ========================== ##
def test_update_call_strategy(strategy):
    '''Test whether method update call strategy properly.'''
    strategy.update_call(input_role='user',output_role='assistant',
                  stop='user',max_token=128,
                  temperature=0.6)
    assert strategy.call.role == {
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.call.stop == 'user'
    assert strategy.call.tokens == 128
    assert strategy.call.temperature == 0.6

def test_update_call_strategy_without_max_token(strategy):
    '''Test whether method show warning without max_token.'''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.update_call(input_role='user',output_role='assistant',
                      stop='user',max_token=0,
                      temperature=0.6)

def test_update_call_strategy_without_stop(strategy):
    '''Test whether method show warning without stop.'''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
            strategy.update_call(input_role='user',output_role='assistant',
                          max_token=128,stop='',
                          temperature=0.6)

## ========================== Update Chat Strategy ========================== ##
def test_update_chat_strategy(strategy):
    '''Test whether method update chat strategy properly.'''
    strategy.update_chat(prompt='You are a kind assistant.',
                  prompt_role='system',input_role='user',output_role='assistant',
                  stop='<|end_of_sentence|>',max_token=128,
                  temperature=1)
    assert strategy.chat.prompt == 'You are a kind assistant.'
    assert strategy.chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.chat.stop == '<|end_of_sentence|>'
    assert strategy.chat.tokens == 128
    assert strategy.chat.temperature == 1

def test_update_chat_strategy_without_max_token(strategy):
    '''Test whether method show warning without max_token.'''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.update_chat(prompt='You are a kind assistant.',
                      prompt_role='system',input_role='user',output_role='assistant',
                      stop='<|end_of_sentence|>',max_token=None,
                      temperature=1)
        
def test_update_call_strategy_without_stop(strategy):
    '''Test whether method show warning without stop.'''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.update_chat(prompt='You are a kind assistant.',
                      prompt_role='system',input_role='user',output_role='assistant',
                      stop=None,max_token=128,
                      temperature=1)