import pytest
from llyra.components import Strategy
from llyra.components.strategys.utils import Call, Chat
from llyra.components.utils import Role
from llyra.errors.components.strategys import StrategySectionMissingError, StrategyParameterMissingError
from pathlib import Path
from re import escape

### ============================= Test Expose Class ============================= ###
@pytest.fixture
def strategy():
    strategy = Strategy()
    return strategy         

@pytest.fixture
def loaded_strategy(tmp_path):
    loaded_strategy = Strategy()
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    loaded_strategy.load(test_strategy)
    return loaded_strategy

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(strategy):
    '''Test whether the class can be initialized properly.'''
    assert strategy.call == None
    assert strategy.chat == None

## ============================= `load()` Method Test ============================= ##
def test_load_method(strategy,tmp_path):
    '''Test whether method can load and read all strategy parameters properly.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0.7)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 'This is for test.','<test-chat-stop-token>',0.8)
    
def test_load_method_without_chat_addition(strategy,tmp_path):
    '''Test whether method can load and read all strategy parameters 
    without chat additional prompt properly.'''
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0.7)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 None,'<test-chat-stop-token>',0.8)    

def test_load_method_without_chat_addition_and_prompt_role(strategy,tmp_path):
    '''Test whether method can load and read all strategy parameters 
    without chat additional prompt and prompt role properly.'''
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0.7)
    assert strategy.chat == Chat(Role(None,'test-input','test-output'),
                                 None,'<test-chat-stop-token>',0.8)

def test_load_method_with_call_stop_fallback(strategy,tmp_path):
    '''Test whether method auto fallback to `[]` and rasie warning 
    when missing `stop` parameter of `call` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    warns_message = 'Missing `stop` parameter of `call` section '
    warns_message += "in `strategy.toml` , auto-fallback to `[]`."
    with pytest.warns(RuntimeWarning,match=escape(warns_message)):
        strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call([],0.7)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 'This is for test.','<test-chat-stop-token>',0.8)
    
def test_load_method_with_call_temperature_fallback(strategy,tmp_path):
    '''Test whether method auto fallback to `0` and rasie warning 
    when missing `temperature` parameter of `call` section.'''
    # Set test prompt file            
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    warns_message = 'Missing `temperature` parameter of `call` section '
    warns_message += "in `strategy.toml` , auto-fallback to `0`."
    with pytest.warns(RuntimeWarning,match=escape(warns_message)):
        strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 'This is for test.','<test-chat-stop-token>',0.8)  

def test_load_method_with_chat_stop_fallback(strategy,tmp_path):
    '''Test whether method auto fallback to `[]` and rasie warning 
    when missing `stop` parameter of `chat` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    warns_message = 'Missing `stop` parameter of `chat` section '
    warns_message += "in `strategy.toml` , auto-fallback to `[]`."
    with pytest.warns(RuntimeWarning,match=escape(warns_message)):
        strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0.7)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 'This is for test.',[],0.8)     
    
def test_load_method_with_chat_temperature_fallback(strategy,tmp_path):
    '''Test whether method auto fallback to `0` and rasie warning 
    when missing `temperature` parameter of `chat` section.'''
    # Set test prompt file            
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    warns_message = 'Missing `temperature` parameter of `chat` section '
    warns_message += "in `strategy.toml` , auto-fallback to `0`."
    with pytest.warns(RuntimeWarning,match=escape(warns_message)):
        strategy.load(test_strategy)
    # Validate loaded value
    assert strategy.call == Call('<test-call-stop-token>',0.7)
    assert strategy.chat == Chat(Role('test-system','test-input','test-output'),
                                 'This is for test.','<test-chat-stop-token>',0)

def test_load_method_with_chat_addition_and_without_prompt_role(strategy,tmp_path):
    '''Test whether method raise exception properly
    without `prompt` parameter in `chat.role` section 
    and with `addition` parameter in `chat` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content     
    with pytest.raises(StrategyParameterMissingError,
        match="Missing `prompt` parameter of `chat.role` section in `strategy.toml`."):
        strategy.load(test_strategy)

def test_load_method_without_input_role_parameter(strategy,tmp_path):
    '''Test whether method raise exception properly 
    without `input` parameter in `chat.role` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(StrategyParameterMissingError,
        match="Missing `input` parameter of `chat.role` section in `strategy.toml`."):
        strategy.load(test_strategy)

def test_load_method_without_output_role_parameter(strategy,tmp_path):
    '''Test whether method raise exception properly 
    without `input` parameter in `chat.role` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file        
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(StrategyParameterMissingError,
        match="Missing `output` parameter of `chat.role` section in `strategy.toml`."):
        strategy.load(test_strategy)

def test_load_method_without_chat_role_section(strategy,tmp_path):
    '''Test whether method raise exception properly 
    without `role` section in `chat` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(StrategySectionMissingError,match='chat.role'):
        strategy.load(test_strategy)

def test_load_method_without_call_section(strategy,tmp_path):
    '''Test whether method raise exception properly 
    without `call` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [chat]
    prompt = "{str(test_prompt)}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(StrategySectionMissingError,match='call'):
        strategy.load(test_strategy)       

def test_load_method_without_chat_section(strategy,tmp_path):
    '''Test whether method raise exception properly 
    without `chat` section.'''
    # Set test prompt file
    content = 'This is for test.'
    test_prompt = tmp_path / 'test.txt'
    test_prompt.write_text(content)
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(StrategySectionMissingError,match='chat'):
        strategy.load(test_strategy)  

def test_load_method_loading_addition_from_error_path(strategy,tmp_path):
    '''Test whether method raise exception properly
    when load additional prompt from error path.'''
    # Set test prompt file path
    test_prompt = 'test.txt'
    # Set test strategy file
    content = f'''
    [call]
    stop = "<test-call-stop-token>"
    temperature = 0.7
    [chat]
    prompt = "{test_prompt}"
    stop = "<test-chat-stop-token>"
    temperature = 0.8
    [chat.role]
    prompt = "test-system"
    input = "test-input"
    output = "test-output"
    '''
    test_strategy = tmp_path / 'test.toml'
    test_strategy.write_text(content)
    # Load test strategy content
    with pytest.raises(FileNotFoundError,
        match='Prompt file not found in provided path.'):
        strategy.load(test_strategy)   

def test_load_method_from_error_path(strategy):
    '''Test whether method raise exception properly
    when load stategy from error path.'''
    # Set test strategy file path
    test_strategy = Path('config/strategy.toml')
    # Load test strategy content
    with pytest.raises(FileNotFoundError,
        match='Strategy file not found in provided path.'):
        strategy.load(test_strategy)           

## ========================== `update_call()` Method Test ========================== ##        
def test_update_call_method(loaded_strategy):
    '''Test whether method can update call strategy parameter properly.'''
    # Execute call strategy update
    loaded_strategy.update_call('<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.call.stop == '<EOF>'
    assert loaded_strategy.call.temperature == 0.1

def test_update_call_method_ignoring_stop_parameters(loaded_strategy):
    '''Test whether method can ignore `stop` parameter and
    update other call strategy parameter at the same time properly.'''
    # Execute call strategy update
    loaded_strategy.update_call(None,0.1)
    # Validate update value
    assert loaded_strategy.call.stop == '<test-call-stop-token>'
    assert loaded_strategy.call.temperature == 0.1

def test_update_call_method_ignoring_temperature_parameters(loaded_strategy):
    '''Test whether method can ignore `temperature` parameter and
    update other call strategy parameter at the same time properly.'''
    # Execute call strategy update
    loaded_strategy.update_call('<EOF>',None)
    # Validate update value
    assert loaded_strategy.call.stop == '<EOF>'
    assert loaded_strategy.call.temperature == 0.7

## ========================== `update_chat()` Method Test ========================== ##
def test_update_chat_method(loaded_strategy):
    '''Test whether method can update chat strategy parameter properly.'''
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                'system','user','assistant',
                                '<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('system','user','assistant')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.1

def test_update_chat_method_ignoring_addition_parameters(loaded_strategy):
    '''Test whether method can ignore `addition` parameter and
    update other chat strategy parameter at the same time properly.'''
    # Execute chat strategy update
    loaded_strategy.update_chat(None,
                                'system','user','assistant',
                                '<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test.'
    assert loaded_strategy.chat.role == Role('system','user','assistant')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.1

def test_update_chat_method_ignoring_prompt_role_parameters(loaded_strategy):
    '''Test whether method can ignore `prompt` parameter of `role` section and
    update other chat strategy parameter at the same time properly.'''    
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                None,'user','assistant',
                                '<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('test-system','user','assistant')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.1

def test_update_chat_method_ignoring_input_role_parameters(loaded_strategy):
    '''Test whether method can ignore `input` parameter of `role` section and
    update other chat strategy parameter at the same time properly.'''    
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                'system',None,'assistant',
                                '<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('system','test-input','assistant')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.1

def test_update_chat_method_ignoring_output_role_parameters(loaded_strategy):
    '''Test whether method can ignore `output` parameter of `role` section and
    update other chat strategy parameter at the same time properly.'''    
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                'system','user',None,
                                '<EOF>',0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('system','user','test-output')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.1

def test_update_chat_method_ignoring_stop_parameters(loaded_strategy):
    '''Test whether method can ignore `stop` parameter and
    update other chat strategy parameter at the same time properly.'''    
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                'system','user','assistant',
                                None,0.1)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('system','user','assistant')
    assert loaded_strategy.chat.stop == '<test-chat-stop-token>'
    assert loaded_strategy.chat.temperature == 0.1   

def test_update_chat_method_ignoring_temperature_parameters(loaded_strategy):
    '''Test whether method can ignore `temperature` parameter and
    update other chat strategy parameter at the same time properly.'''    
    # Execute chat strategy update
    loaded_strategy.update_chat('This is for test/2',
                                'system','user','assistant',
                                '<EOF>',None)
    # Validate update value
    assert loaded_strategy.chat.addition == 'This is for test/2'
    assert loaded_strategy.chat.role == Role('system','user','assistant')
    assert loaded_strategy.chat.stop == '<EOF>'
    assert loaded_strategy.chat.temperature == 0.8 

def test_update_chat_method_allowing_prompt_role_empty_without_addition(loaded_strategy):
    '''Test whether method can set `prompt` parameter of `role` section empty 
    when chat addition is empty or is set to empty at the same time properly.'''
    # Execute chat strategy update
    loaded_strategy.update_chat('','',None,None,None,None)
    # Validate update value
    assert not loaded_strategy.chat.addition
    assert loaded_strategy.chat.role == Role('','test-input','test-output')

def test_update_chat_method_forbidding_prompt_role_empty_with_addition(loaded_strategy):
    '''Test whether method raise exception properly
    when set `prompt` parameter of `role` section to empty 
    with chat additional prompt.'''
    error = "`prompt` parameter of `chat.role` setting can't be empty "
    error += "when `addition` parameter of `chat` setting isn't empty. "
    with pytest.raises(ValueError,match=error):
        loaded_strategy.update_chat(None,'',None,None,None,None)