import pytest
from llyra.local.strategys import Strategy
import warnings,json

@pytest.fixture
def strategy():
    strategy = Strategy()
    return strategy

## ========================== Initialize Test ========================== ##
def test_class_initialize(strategy):
    '''Test whether the class can be initialized properly.'''
    assert strategy.call_role == {
        'input': None,
        'output': None
        }
    assert strategy.call_stop == None
    assert strategy.call_tokens == None
    assert strategy.call_temperature == None

## ========================== Load Method Test ========================== ##
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

def test_load_strategy_with_wrong_path(strategy):
    '''Test whether method raise exception when file path error. '''
    error = 'Error: Strategy file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy.load('tests/strategy/strategy.json')

def test_load_strategy_with_invalid_format(strategy):
    '''Test whether method raise excepetion when strategy format error.'''
    error = 'Error: Stratgy should be a list.'
    with pytest.raises(IsADirectoryError,match=error):
        strategy.load('tests/strategys/strategy_format_error.json')

def test_load_strategy_with_missing_type(strategy):
    '''Test whether method raise excepetion when missing keys.'''
    error = 'Error: Invalid strategy format.'
    with pytest.raises(KeyError,match=error):
        strategy.load('tests/strategys/strategy_missing_type.json')

def test_load_strategy_with_no_call_input_role(strategy):
    '''
    Test whether method show warning with no input role for call.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing input role parameter for call inference.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_input_role.json')
        assert strategy.call_role == {
            'input': None,
            'output': "<|Assistant|>"
            }
        assert strategy.call_stop == "<|User|>"
        assert strategy.call_tokens == 128e3
        assert strategy.call_temperature == 0.6

def test_load_strategy_with_no_call_output_role(strategy):
    '''
    Test whether method show warning with no output role for call.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing output role parameter for call inference.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/strategy_no_call_output_role.json')
        assert strategy.call_role == {
            'input': "<|User|>",
            'output': None
            }
        assert strategy.call_stop == "<|User|>"
        assert strategy.call_tokens == 128e3
        assert strategy.call_temperature == 0.6

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
        assert strategy.call_role == {
            'input': "<|User|>",
            'output': "<|Assistant|>"
            }
        assert strategy.call_stop == "<|User|>"
        assert strategy.call_tokens == None
        assert strategy.call_temperature == 0.6

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
        assert strategy.call_role == {
            'input': "<|User|>",
            'output': "<|Assistant|>"
            }
        assert strategy.call_stop == None
        assert strategy.call_tokens == 128e3
        assert strategy.call_temperature == 0.6

def test_load_strategy_with_no_call_temperature(strategy):
    '''Test whether method load call strategy witout temperature from path properly.'''
    strategy.load('tests/strategys/strategy_no_call_temperature.json')
    assert strategy.call_role == {
        'input': "<|User|>",
        'output': "<|Assistant|>"
        }
    assert strategy.call_stop == "<|User|>"
    assert strategy.call_tokens == 128e3
    assert strategy.call_temperature == 0

## ========================== Update Method Test ========================== ##
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

def test_update_call_strategy_without_max_token(strategy):
    '''Test whether method show warning without max_token.'''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.call(input_role='user',output_role='assistant',
                      stop='user',max_token=0,
                      temperature=0.6)

def test_update_call_strategy_without_stop(strategy):
    '''Test whether method show warning without stop.'''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
            strategy.call(input_role='user',output_role='assistant',
                          max_token=128,stop='',
                          temperature=0.6)