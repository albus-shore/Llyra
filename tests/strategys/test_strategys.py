import pytest
from llyra.local.strategys import Strategy
import warnings,json

@pytest.fixture
def strategy():
    strategy = Strategy()
    return strategy

### =============================== Initialize Test =============================== ###
def test_class_initialize(strategy):
    '''Test whether the class can be initialized properly.'''
    assert strategy.call_role == {
        'input': None,
        'output': None
        }
    assert strategy.call_stop == None
    assert strategy.call_tokens == None
    assert strategy.call_temperature == None
    assert strategy.chat_prompt == None
    assert strategy.chat_role == {
        'input': None,
        'output': None
        }
    assert strategy.chat_stop == None
    assert strategy.chat_tokens == None
    assert strategy.chat_temperature == None

### =============================== Load Method Test =============================== ###
def test_load_strategy_file(strategy):
    '''Test whether method load strategy file form path properly.'''
    strategy.load('tests/strategys/strategy_normal.json')
    assert strategy.call_role == {
        'input': "<|User|>",
        'output': "<|Assistant|>"
        }
    assert strategy.call_stop == "<|User|>"
    assert strategy.call_tokens == 128e3
    assert strategy.call_temperature == 0.6
    assert strategy.chat_prompt == ''
    assert strategy.chat_role == {
        'input': '<|User|>',
        'output': '<|Assistant|>'
        }
    assert strategy.chat_stop == "<|User|>"
    assert strategy.chat_tokens == 128000
    assert strategy.chat_temperature == 0.6

def test_load_strategy_with_wrong_path(strategy):
    '''Test whether method raise exception when file path error. '''
    error = 'Error: Strategy file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy.load('tests/strategy/strategy.json')

## ======================== Call Strategy Load Error Test ======================== ##
def test_load_strategy_with_invalid_format(strategy):
    '''Test whether method raise excepetion when strategy format error.'''
    error = 'Error: Stratgy should be a list.'
    with pytest.raises(IsADirectoryError,match=error):
        strategy.load('tests/strategys/strategy_call_format_error.json')

def test_load_strategy_with_missing_keys(strategy):
    '''Test whether method raise excepetion when missing keys.'''
    error = 'Error: Invalid strategy formate.'
    with pytest.raises(KeyError,match=error):
        strategy.load('tests/strategys/strategy_call_missing_keys.json')

def test_load_strategy_with_empty_input_role(strategy):
    '''Test whether method raise exception with empty input role.'''
    warning = 'Warning: Error set input role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_call_empty_input_role.json')

def test_load_strategy_with_empty_output_role(strategy):
    '''Test whether method raise exception with empty output role.'''
    warning = 'Warning: Error set output role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_call_empty_output_role.json')

def test_load_strategy_with_empty_max_token(strategy):
    '''Test whether method show warning with empty max_token.'''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_call_empty_max_token.json')

def test_load_strategy_with_empty_stop(strategy):
    '''Test whether method show warning with empty stop.'''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_call_empty_stop.json')

## ======================== Chat Strategy Load Error Test ======================== ##
def test_load_strategy_with_invalid_format(strategy):
    '''Test whether method raise excepetion when strategy format error.'''
    error = 'Error: Stratgy should be a list.'
    with pytest.raises(IsADirectoryError,match=error):
        strategy.load('tests/strategys/strategy_chat_format_error.json')

def test_load_strategy_with_missing_keys(strategy):
    '''Test whether method raise excepetion when missing keys.'''
    error = 'Error: Invalid strategy formate.'
    with pytest.raises(KeyError,match=error):
        strategy.load('tests/strategys/strategy_chat_missing_keys.json')

def test_load_strategy_with_error_prompt_path(strategy):
    '''Test whether method raise exception when prompt path error.'''
    error = 'Error: Prompt file not found.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy.load('tests/strategys/strategy_chat_error_prompt.json')

def test_load_strategy_with_no_prompt(strategy):
    '''Test whether method not raise exception when prompt is empty 
        or not provided.
    '''
    strategy.load('tests/strategys/strategy_chat_no_prompt.json')
    strategy.load('tests/strategys/strategy_chat_empty_prompt.json')

def test_load_strategy_with_empty_input_role(strategy):
    '''Test whether method raise exception with empty input role.'''
    warning = 'Warning: Error set input role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_chat_empty_input_role.json')

def test_load_strategy_with_empty_output_role(strategy):
    '''Test whether method raise exception with empty output role.'''
    warning = 'Warning: Error set output role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_chat_empty_output_role.json')

def test_load_strategy_with_empty_max_token(strategy):
    '''Test whether method show warning with empty max_token.'''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_chat_empty_max_token.json')

def test_load_strategy_with_empty_stop(strategy):
    '''Test whether method show warning with empty stop.'''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_chat_empty_stop.json')

### ============================== Update Method Test ============================== ###
## ========================== Call Strategy Update Test ========================== ##
def test_update_call_strategy(strategy):
    '''Test whether method update call strategy properly.'''
    strategy.call(input_role='user',output_role='assistant',
                  stop='user',max_token=128,
                  temperature=0.6)
    assert strategy.call_role == {
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.call_stop == 'user'
    assert strategy.call_tokens == 128
    assert strategy.call_temperature == 0.6

def test_update_call_strategy_without_necessary_inputs(strategy):
    '''Test whether method show warning without necessary inputs.'''
    # Test missing input role
    warning = 'Warning: Error set input role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.call(input_role='',output_role='assistant',
                    stop='user',max_token=128,
                    temperature=0.6)
        assert strategy.call_role == {
            'input': '',
            'output': 'assistant'
            }
        assert strategy.call_stop == 'user'
        assert strategy.call_tokens == 128
        assert strategy.call_temperature == 0.6
    # Test missing output role
    warning = 'Warning: Error set output role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.call(input_role='user',output_role='',
                      stop='user',max_token=128,
                      temperature=0.6)
        assert strategy.call_role == {
            'input': 'user',
            'output': ''
            }
        assert strategy.call_stop == 'user'
        assert strategy.call_tokens == 128
        assert strategy.call_temperature == 0.6
    # Test missing stop
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.call(input_role='user',output_role='assistant',
                      max_token=128,stop='',
                      temperature=0.6)
        assert strategy.call_role == {
            'input': 'user',
            'output': 'assistant'
            }
        assert strategy.call_stop == ''
        assert strategy.call_tokens == 128
        assert strategy.call_temperature == 0.6
    # Test missing max token
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.call(input_role='user',output_role='assistant',
                      stop='user',max_token=0,
                      temperature=0.6)
        assert strategy.call_role == {
            'input': 'user',
            'output': 'assistant'
            }
        assert strategy.call_stop == 'user'
        assert strategy.call_tokens == 0
        assert strategy.call_temperature == 0.6
        
def test_call_strategy_temperature_is_none(strategy):    
    '''Test whether method raise exception when temperature is None.'''
    error = 'Error: Inference temperature must be set.'
    with pytest.raises(ValueError,match=error):
        strategy.call(input_role='user',output_role='assistant',
                      max_token=128,stop='user',
                      temperature=None)

## ========================== Chat Strategy Update Test ========================== ##
def test_update_chat_strategy(strategy):
    '''Test whether method chat strategy properly.'''
    strategy.chat(prompt='Your are a assistant.',
                  input_role='<|User|>',output_role='<|Assistant|>',
                  stop='<|User|>',max_token=128e3,
                  temperature=0.6)
    assert strategy.chat_prompt == 'Your are a assistant.'
    assert strategy.chat_role == {
        'input': '<|User|>',
        'output': '<|Assistant|>',
        }
    assert strategy.chat_stop == '<|User|>'
    assert strategy.chat_tokens == 128e3
    assert strategy.chat_temperature == 0.6

def test_update_chat_strategy_without_necessary_inputs(strategy):
    '''Test whether method show warning without necessary inputs.'''
    # Test missing input role
    warning = 'Warning: Error set input role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.chat(prompt='Your are a assistant.',
                      input_role='',output_role='<|Assistant|>',
                      stop='<|User|>',max_token=128e3,
                      temperature=0.6)
        assert strategy.chat_prompt == 'Your are a assistant.'
        assert strategy.chat_role == {
            'input': '',
            'output': '<|Assistant|>',
            }
        assert strategy.chat_stop == '<|User|>'
        assert strategy.chat_tokens == 128e3
        assert strategy.chat_temperature == 0.6
    # Test missing output role
    warning = 'Warning: Error set output role indicate token, '
    warning += 'model inference may not behave properly.'
    with pytest.warns(UserWarning,match=warning):
        strategy.chat(prompt='Your are a assistant.',
                      input_role='<|User|>',output_role='',
                      stop='<|User|>',max_token=128e3,
                      temperature=0.6)
        assert strategy.chat_prompt == 'Your are a assistant.'
        assert strategy.chat_role == {
            'input': '<|User|>',
            'output': '',
            }
        assert strategy.chat_stop == '<|User|>'
        assert strategy.chat_tokens == 128e3
        assert strategy.chat_temperature == 0.6
    # Test missing stop
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.chat(prompt='Your are a assistant.',
                  input_role='<|User|>',output_role='<|Assistant|>',
                  stop='',max_token=128e3,
                  temperature=0.6)
        assert strategy.chat_prompt == 'Your are a assistant.'
        assert strategy.chat_role == {
            'input': '<|User|>',
            'output': '<|Assistant|>',
            }
        assert strategy.chat_stop == ''
        assert strategy.chat_tokens == 128e3
        assert strategy.chat_temperature == 0.6
    # Test missing max token
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.chat(prompt='Your are a assistant.',
                      input_role='<|User|>',output_role='<|Assistant|>',
                      stop='<|User|>',max_token=0,
                      temperature=0.6)
        assert strategy.chat_prompt == 'Your are a assistant.'
        assert strategy.chat_role == {
            'input': '<|User|>',
            'output': '<|Assistant|>',
            }
        assert strategy.chat_stop == '<|User|>'
        assert strategy.chat_tokens == 0
        assert strategy.chat_temperature == 0.6
    
def test_chat_strategy_temperature_is_none(strategy):
    '''Test whether method raise exception when temperature is None.'''
    error = 'Error: Inference temperature must be set.'
    with pytest.raises(ValueError,match=error):
        strategy.chat(prompt='Your are a assistant.',
                      input_role='<|User|>',output_role='<|Assistant|>',
                      stop='<|User|>',max_token=128e3,
                      temperature=None)