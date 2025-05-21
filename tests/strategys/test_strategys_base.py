import pytest
from llyra.base import Strategy
from llyra.base.strategys import _Call, _Chat

### ============================ Test Internal Class ============================ ###
## =============================== _Call Class =============================== ##
# ============================= Initialize Test ============================= #
def test_call_class_initialize():
    '''Test whether the class can be initialized properly.'''
    call = _Call()

## =============================== _Chat Class =============================== ##
@pytest.fixture
def chat():
    chat = _Chat()
    return chat
# ============================= Initialize Test ============================= #
def test_chat_class_initialize(chat):
    '''Test whether the class can be initialized properly.'''
    assert chat.prompt == None
    assert chat.role == {
        'prompt': None,
        'input': None,
        'output': None,    
        }
    
# ============================ Load Method Test ============================ #
def test_chat_load_basic_strategy(chat):
    '''Test whether method load basic strategy form input properly.'''
    test_content = {
        "role": {
            "prompt": "system",
            "input": "user",
            "output": "assistant"
            },
        "prompt": "tests/strategys/prompt.txt",
    }
    chat.load(test_content)
    assert chat.prompt == 'This is used for test.'
    assert chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant'
        }

def test_chat_load_basic_strategy_with_no_prompt(chat):
    '''Test whether method load basic strategy without prompt form input properly.'''
    test_content = {
        "role": {
            "input": "user",
            "output": "assistant"
            },
    }
    chat.load(test_content)
    assert chat.prompt == None
    assert chat.role == {
        'prompt': None,
        'input': 'user',
        'output': 'assistant'
        }

def test_chat_load_basic_strategy_with_wrong_prompt_path(chat):
    '''Test whether method raise exception when prompt path incorrect.'''
    test_content = {
        "role": {
            "prompt": "system",
            "input": "user",
            "output": "assistant"
            },
        "prompt": "tests/strategy/prompt.txt",
    }
    error = 'Error: Prompt file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        chat.load(test_content)

def test_chat_load_basic_strategy_with_no_chat_prompt_role(chat):
    '''Test whether method raise exception with no prompt role for chat.'''
    test_content = {
        "role": {
            "input": "user",
            "output": "assistant"
            },
        "prompt": "tests/strategys/prompt.txt",
    }
    error = 'Error: Missing prompt role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.load(test_content)

def test_chat_load_basic_strategy_with_no_chat_input_role(chat):
    '''Test whether method raise exception with no input role for chat.'''
    test_content = {
        "role": {
            "prompt": "system",
            "output": "assistant"
            },
        "prompt": "tests/strategys/prompt.txt",
    }
    error = 'Error: Missing input role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.load(test_content)

def test_chat_load_basic_strategy_with_no_chat_output_role(chat):
    '''Test whether method raise exception with no output role for chat.'''
    test_content = {
        "role": {
            "prompt": "system",
            "input": "user",
            },
        "prompt": "tests/strategys/prompt.txt",
    }
    error = 'Error: Missing output role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.load(test_content)

# =========================== Update Method Test =========================== #
def test_chat_update_basic_strategy(chat):
    '''Test whether method update basic strategy form input properly.'''
    chat.update(prompt='This is used for test.',
        prompt_role='system',input_role='user',output_role='assistant')
    assert chat.prompt == 'This is used for test.'
    assert chat.role == {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant'
        }
    
def test_chat_update_basic_strategy_with_no_prompt(chat):
    '''Test whether method update basic strategy without prompt form input properly.'''
    chat.update(prompt=None,
        prompt_role=None,input_role='user',output_role='assistant')
    assert chat.prompt == None
    assert chat.role == {
        'prompt': None,
        'input': 'user',
        'output': 'assistant'
        }

def test_chat_update_basic_strategy_with_no_chat_prompt_role(chat):
    '''Test whether method raise exception with no prompt role for chat.'''
    error = 'Error: Missing prompt role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.update(prompt='This is used for test.',
            prompt_role=None,input_role='user',output_role='assistant')

def test_chat_update_basic_strategy_with_no_chat_input_role(chat):
    '''Test whether method raise exception with no input role for chat.'''
    error = 'Error: Missing input role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.update(prompt='This is used for test.',
            prompt_role='system',input_role=None,output_role='assistant')

def test_chat_update_basic_strategy_with_no_chat_output_role(chat):
    '''Test whether method raise exception with no output role for chat.'''
    error = 'Error: Missing output role parameter for chat inference.'
    with pytest.raises(ValueError,match=error):
        chat.update(prompt='This is used for test.',
            prompt_role='system',input_role='user',output_role=None)

### ============================= Test Expose Class ============================= ###
@pytest.fixture
def strategy():
    strategy = Strategy()
    return strategy
# ============================= Initialize Test ============================= #
def test_class_initialize(strategy):
    '''Test whether the class can be initialized properly.'''
    assert isinstance(strategy.call,_Call) == True
    assert strategy.chat.prompt == None
    assert strategy.chat.role == {
            'prompt': None,
            'input': None,
            'output': None,
            }

# ============================ Load Method Test ============================ #
def test_call(strategy:str):
    pass
def test_chat(strategy:str):
    pass

def test_load_strategy_file(strategy):
    '''Test whether method load strategy file form path properly.'''
    strategy._load('tests/strategys/strategy_base.json',test_call,test_chat)
    assert isinstance(strategy.call,_Call) == True
    assert strategy.chat.prompt == 'This is used for test.'
    assert strategy.chat.role == {
            'prompt': 'system',
            'input': 'user',
            'output': 'assistant',
            }

def test_load_strategy_with_wrong_path(strategy):
    '''Test whether method raise exception when file path error. '''
    error = 'Error: Strategy file not found in provided path.'
    with pytest.raises(FileNotFoundError,match=error):
        strategy._load('tests/strategys/strategy.json',test_call,test_chat)

def test_load_strategy_with_invalid_format(strategy):
    '''Test whether method raise excepetion when strategy format error.'''
    error = 'Error: Stratgy should be a list.'
    with pytest.raises(IsADirectoryError,match=error):
        strategy._load('tests/strategys/strategy_format_error.json',test_call,test_chat)

def test_load_strategy_with_missing_type(strategy):
    '''Test whether method raise excepetion when missing keys.'''
    error = 'Error: Invalid strategy format.'
    with pytest.raises(KeyError,match=error):
        strategy._load('tests/strategys/strategy_missing_type.json',test_call,test_chat)                                         