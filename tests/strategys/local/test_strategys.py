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
    strategy.load('tests/strategys/local/strategy_normal.json')
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

def test_load_strategy_with_wrong_path(strategy):
    '''Test whether method raise exception when file path error. '''
    error = 'Error: Strategy file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy.load('tests/strategy/strategy.json')

def test_load_strategy_with_invalid_format(strategy):
    '''Test whether method raise excepetion when strategy format error.'''
    error = 'Error: Stratgy should be a list.'
    with pytest.raises(IsADirectoryError,match=error):
        strategy.load('tests/strategys/local/strategy_format_error.json')

def test_load_strategy_with_missing_type(strategy):
    '''Test whether method raise excepetion when missing keys.'''
    error = 'Error: Invalid strategy format.'
    with pytest.raises(KeyError,match=error):
        strategy.load('tests/strategys/local/strategy_missing_type.json')

## ========================== Load Call Strategy ========================== ##
def test_load_strategy_with_no_call_input_role(strategy):
    '''
    Test whether method show warning with no input role for call.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing input role parameter for call inference.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/local/strategy_no_call_input_role.json')
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
        strategy.load('tests/strategys/local/strategy_no_call_output_role.json')
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
        strategy.load('tests/strategys/local/strategy_no_call_max_token.json')
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
        strategy.load('tests/strategys/local/strategy_no_call_stop.json')
        assert strategy.call.role == {
            'input': "<|User|>",
            'output': "<|Assistant|>"
            }
        assert strategy.call.stop == None
        assert strategy.call.tokens == 128e3
        assert strategy.call.temperature == 0.6

def test_load_strategy_with_no_call_temperature(strategy):
    '''Test whether method load call strategy witout temperature from path properly.'''
    strategy.load('tests/strategys/local/strategy_no_call_temperature.json')
    assert strategy.call.role == {
        'input': "<|User|>",
        'output': "<|Assistant|>"
        }
    assert strategy.call.stop == "<|User|>"
    assert strategy.call.tokens == 128e3
    assert strategy.call.temperature == 0

## ========================== Load Chat Strategy ========================== ##
def test_load_strategy_with_no_chat_prompt(strategy):
    '''Test whether method load chat strategy without prompt from path properly.'''
    strategy.load('tests/strategys/local/strategy_no_chat_prompt.json')
    assert strategy.chat.prompt == None
    assert strategy.chat.role == {
        'prompt': None,
        'input': 'user',
        'output': 'assistant'
        }
    assert strategy.chat.stop == '<|User|>'
    assert strategy.chat.tokens == 128e3
    assert strategy.chat.temperature == 0.6

def test_load_strategy_with_error_chat_prompt(strategy):
    '''Test whether method raise exception when prompt path error.'''
    error = 'Error: Prompt file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy.load('tests/strategys/local/strategy_error_chat_prompt.json')
    
def test_load_strategy_with_no_chat_prompt_role(strategy):
    '''Test whether method raise exception with no prompt role for chat.'''
    error = 'Error: Missing prompt role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.load('tests/strategys/local/strategy_no_chat_prompt_role.json')

def test_load_strategy_with_no_chat_input_role(strategy):
    '''Test whether method raise exception with no input role for chat.'''
    error = 'Error: Missing input role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.load('tests/strategys/local/strategy_no_chat_input_role.json')

def test_load_strategy_with_no_chat_output_role(strategy):
    '''Test whether method raise exception with no output role for chat.'''
    error = 'Error: Missing output role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.load('tests/strategys/local/strategy_no_chat_output_role.json')

def test_load_strategy_with_no_chat_max_token(strategy):
    '''
    Test whether method show warning with no max_token.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Error set max token strategy parameter, '
    warning += 'the max generation token number will be set '
    warning += 'refer to the loaded model.'
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/local/strategy_no_chat_max_token.json')
        assert strategy.chat.prompt == 'This is used for test.'
        assert strategy.chat.role == {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant'
            }
        assert strategy.chat.stop == '<|User|>'
        assert strategy.chat.tokens == None
        assert strategy.chat.temperature == 0.6

def test_load_strategy_with_chat_no_stop(strategy):
    '''
    Test whether method show warning with no stop.
    And load strategy file form path properly.
    '''
    warning = 'Warning: Missing stop strategy parameter, '
    warning += "inference won't stop "
    warning += "until max generation token number reached."
    with pytest.warns(UserWarning,match=warning):
        strategy.load('tests/strategys/local/strategy_no_chat_stop.json')
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
    strategy.load('tests/strategys/local/strategy_no_chat_temperature.json')
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

def test_update_chat_strategy_with_empty_prompt_role(strategy):
    '''Test whether method refused to update prompt role when its input is empty.'''
    error = 'Error: Missing prompt role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.update_chat(prompt='You are a kind assistant.',
                  prompt_role='',input_role='user',output_role='assistant',
                  stop='<|end_of_sentence|>',max_token=128,
                  temperature=1)

def test_update_chat_strategy_with_empty_input_role(strategy):
    '''Test whether method refused to update input role when its input is empty.'''
    error = 'Error: Missing input role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.update_chat(prompt='You are a kind assistant.',
                  prompt_role='system',input_role='',output_role='assistant',
                  stop='<|end_of_sentence|>',max_token=128,
                  temperature=1)


def test_update_chat_strategy_with_empty_output_role(strategy):
    '''Test whether method refused to update output role when its input is empty.'''
    error = 'Error: Missing output role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        strategy.update_chat(prompt='You are a kind assistant.',
                  prompt_role='system',input_role='user',output_role='',
                  stop='<|end_of_sentence|>',max_token=128,
                  temperature=1)

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