import pytest
from llyra.components.strategys import Strategy
from llyra.data.components import StrategyData
from llyra.data.components.startegys.untils.classes import CallStrategyData, \
    ChatStrategyData
from llyra.data.components.utils.roles import Role
from llyra.exceptions.components.strategys import StrategyOutOfRangeError, \
    StrategyParameterMissingError, StrategySectionMissingError, \
    StrategyCrashError, StrategyNoAvailableModeError
from re import escape
from tomllib import load as load_toml
from tomli_w import dumps as dump_toml

## ================================= Test instance ================================= ##
@pytest.fixture
def strategy():
    return Strategy()

## ============================== Test strategy file ============================== ##
@pytest.fixture
def strategy_path(tmp_path):
    # Build test extra prompt
    test_prompt = 'Test content.'
    test_prompt_path = tmp_path / 'text.txt'
    test_prompt_path.write_text(test_prompt)
    # Build test strategy
    test_strategy = f'''
    [call]
    stop = "test-stop-call"
    temperature = 0.6

    [chat]
    prompt = "{str(test_prompt_path)}"
    stop = "test-stop-chat"
    temperature = 0.5

    [chat.role]
    prompt = "system"
    input = "user"
    output = "assistant"
    '''
    # Build & Return test strategy file
    test_path = tmp_path / 'test.toml'
    test_path.write_text(test_strategy)
    return test_path

## ============================== Test `load` method ============================== ##
def test_method_load_with_wrong_path(strategy,tmp_path):
    # Build test path
    test_path = tmp_path / 'test.toml'
    # Check exception raise
    with pytest.raises(FileNotFoundError,match='Strategy File Not Found.'):
        strategy.load(path=test_path)

test_method_load_normal_cases = [([],
                                  StrategyData(
                                      call=CallStrategyData(
                                        stop='test-stop-call',
                                        temperature=0.6),
                                      chat=ChatStrategyData(
                                          role=Role(prompt='system',
                                                    input='user',
                                                    output='assistant'),
                                          prompt='Test content.',
                                          stop='test-stop-chat',
                                          temperature=0.5))),
                                 (['chat.prompt'],
                                  StrategyData(
                                      call=CallStrategyData(
                                        stop='test-stop-call',
                                        temperature=0.6),
                                      chat=ChatStrategyData(
                                          role=Role(prompt='system',
                                                    input='user',
                                                    output='assistant'),
                                          prompt=False,
                                          stop='test-stop-chat',
                                          temperature=0.5)))]
@pytest.mark.parametrize(['changing_keys','ground_truth'],
                         test_method_load_normal_cases)
def test_method_load_normal(strategy,strategy_path,
                            changing_keys:list,ground_truth:StrategyData):
    # Read original strategy 
    with strategy_path.open('rb') as obj:
        test_strategy:dict = load_toml(obj)
    # Remove missing section or parameter
    for changing_key in changing_keys:
        keys:list = changing_key.split('.')
        if len(keys) == 1:
            test_strategy.pop(keys[0])
        elif len(keys) == 2:
            test_strategy[keys[0]].pop(keys[1])
        elif len(keys) == 3:
            test_strategy[keys[0]][keys[1]].pop(keys[2])
    # Update strategy file
    strategy_path.write_text(dump_toml(test_strategy))
    # Check load result
    result = strategy.load(strategy_path)
    assert result == ground_truth

test_method_load_warn_cases = [
    (['call'],
    ('Missing `call` section in strategy file.\n'
     '`call` inference not available.'),
     StrategyData(call=False,
                  chat=ChatStrategyData(
                      role=Role(prompt='system',
                                input='user',
                                output='assistant'),
                      prompt='Test content.',
                      stop='test-stop-chat',
                      temperature=0.5))),
    (['call','chat.prompt'],
    ('Missing `call` section in strategy file.\n'
     '`call` inference not available.'),
     StrategyData(call=False,
                  chat=ChatStrategyData(
                      role=Role(
                          prompt='system',
                          input='user',
                          output='assistant'),
                      prompt=False,
                      stop='test-stop-chat',
                      temperature=0.5))),
    (['chat'],
    ('Missing `chat` section in strategy file.\n'
     '`chat` inference not available.'),
     StrategyData(
         call=CallStrategyData(
             stop='test-stop-call',
             temperature=0.6),
             chat=False)),
    (['chat.role.prompt','chat.prompt'],
     ('Missing `prompt` parameter in `chat.role` section in strategy file.\n'
      'Extra prompt not available(Crashing Exception).'),
     StrategyData(
         call=CallStrategyData(
             stop='test-stop-call',
             temperature=0.6),
         chat=ChatStrategyData(
             role=Role(prompt=False,
                       input='user',
                       output='assistant'),
             prompt=False,
             stop='test-stop-chat',
             temperature=0.5)))]
@pytest.mark.parametrize(['changing_keys','message','ground_truth'],
                         test_method_load_warn_cases)
def test_method_load_warn(strategy,strategy_path,
                          changing_keys,message,ground_truth):
    # Read original strategy 
    with strategy_path.open('rb') as obj:
        test_strategy:dict = load_toml(obj)
    # Remove missing section or parameter
    for changing_key in changing_keys:
        keys:list = changing_key.split('.')
        if len(keys) == 1:
            test_strategy.pop(keys[0])
        elif len(keys) == 2:
            test_strategy[keys[0]].pop(keys[1])
        elif len(keys) == 3:
            test_strategy[keys[0]][keys[1]].pop(keys[2])
    # Update strategy file
    strategy_path.write_text(dump_toml(test_strategy))
    # Check warning showing
    with pytest.warns(RuntimeWarning,match=escape(message)):
        result = strategy.load(strategy_path)
    # Check load result
    assert result == ground_truth

test_method_load_raise_cases = [
    (['call.stop'],
     StrategyParameterMissingError,
     'Missing `stop` parameter in `call` section in strategy file.'),
    (['call.temperature'],
     StrategyParameterMissingError,
     'Missing `temperature` parameter in `call` section in strategy file.'),
    (['chat.role'],
     StrategySectionMissingError,
     'Missing `chat.role` section in strategy file.'),
    (['chat.role.input'],
     StrategyParameterMissingError,
     'Missing `input` parameter in `chat.role` section in strategy file.'),
    (['chat.role.output'],
     StrategyParameterMissingError,
     'Missing `output` parameter in `chat.role` section in strategy file.'),
    (['chat.role.prompt'],
     StrategyCrashError,
     ('`prompt` parameter not provided in `chat.role` section '
      'or being manually set via methods.\n'
      'Extra prompt not available.')),
    (['chat.stop'],
     StrategyParameterMissingError,
     'Missing `stop` parameter in `chat` section in strategy file.'),
    (['chat.temperature'],
     StrategyParameterMissingError,
     'Missing `temperature` parameter in `chat` section in strategy file.'),
    (['call','chat'],
     StrategyNoAvailableModeError,
     ('Neither `call` or `chat` section is found in strategy file.'
      'No inference mode available.\n'
      'Note: You can not initialize strategy sections after instance creation.'))]
@pytest.mark.parametrize(['changing_keys','exception','message'],
                         test_method_load_raise_cases)
def test_method_load_raise(strategy,strategy_path,
                           changing_keys,exception,message):
    # Read original strategy 
    with strategy_path.open('rb') as obj:
        test_strategy:dict = load_toml(obj)
    # Remove missing section or parameter
    for changing_key in changing_keys:
        keys:list = changing_key.split('.')
        if len(keys) == 1:
            test_strategy.pop(keys[0])
        elif len(keys) == 2:
            test_strategy[keys[0]].pop(keys[1])
        elif len(keys) == 3:
            test_strategy[keys[0]][keys[1]].pop(keys[2])
    # Update strategy file
    strategy_path.write_text(dump_toml(test_strategy))
    # Check exception raise
    with pytest.raises(exception,match=escape(message)):
        strategy.load(strategy_path)

def test_method_load_with_wrong_prompt_path(strategy,strategy_path):
    # Read original strategy 
    with strategy_path.open('rb') as obj:
        test_strategy:dict = load_toml(obj)
    # Build test path
    test_strategy['chat']['prompt'] = 'tests/test.txt'
    # Update strategy file
    strategy_path.write_text(dump_toml(test_strategy))
    # Check exception raise
    with pytest.raises(FileNotFoundError,match='Prompt File Not Found.'):
        strategy.load(strategy_path)

## ============================== Test `call` method ============================== ##
def test_method_call_raise(strategy):
    with pytest.raises(StrategyOutOfRangeError,
        match=('`call` strategy section uninitialized '
                     'due to lack of related section in strategy file.\n'
                     'You can not initialize it and modify any parameter within it '
                     'by methods during runtime.')):
        strategy.call(strategy=StrategyData(call=False,
                                            chat=ChatStrategyData(
                                                role=Role(
                                                    prompt='system',
                                                    input='user',
                                                    output='assistant'),
                                                prompt='Test content.',
                                                stop='test-stop-chat',
                                                temperature=0.5)))

test_method_call_normal_cases = [(
    StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=ChatStrategyData(role=Role(prompt='system',
                                        input='user',
                                        output='assistant'),
                              prompt='Test content.',
                              stop='test-stop-chat',
                              temperature=0.5)),
    False,False,
    StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=ChatStrategyData(role=Role(prompt='system',
                                        input='user',
                                        output='assistant'),
                              prompt='Test content.',
                              stop='test-stop-chat',
                              temperature=0.5))),
    (StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=False),
    False,False,
    StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=False)),
    (StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=False),
    'modified-test-stop',False,
    StrategyData(
        call=CallStrategyData(stop='modified-test-stop',temperature=0.6),
        chat=False)),
    (StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=0.6),
        chat=False),
    False,1.0,
    StrategyData(
        call=CallStrategyData(stop='test-stop-call',temperature=1.0),
        chat=False))]
@pytest.mark.parametrize(['original_strategy','stop','temperature','ground_truth'],
                         test_method_call_normal_cases)
def test_method_call_normal(strategy,
                            original_strategy,stop,temperature,ground_truth):
    result = strategy.call(strategy=original_strategy,
                           stop=stop,temperature=temperature)
    assert result == ground_truth

## ============================== Test `chat` method ============================== ##
def test_method_chat_with_False_chat_section(strategy):
    with pytest.raises(StrategyOutOfRangeError,
        match=('`chat` strategy section uninitialized '
               'due to lack of related section in strategy file.\n'
               'You can not initialize it and modify any parameter within it '
               'by methods during runtime.')):
        strategy.chat(strategy=StrategyData(call=CallStrategyData(
                                                stop='test-stop-call',
                                                temperature=0.6),
                                            chat=False))
        
def test_method_chat_with_False_prompt_role_and_extra_prompt(strategy):
    with pytest.raises(StrategyCrashError,
                       match=('`prompt` parameter not provided in `chat.role` section '
                              'or being manually set via methods.\n'
                              'Extra prompt not available.')):
        strategy.chat(
            strategy=StrategyData(
                call=CallStrategyData(
                    stop='test-stop-call',
                    temperature=0.6),
                chat=ChatStrategyData(
                    role=Role(
                        prompt=False,
                        input='user',
                        output='assistant'),
                prompt=False,
                stop='test-stop-chat',
                temperature=0.5)),
            prompt='Test content.')
        
test_method_chat_normal_cases = [(
    StrategyData(
        call=CallStrategyData(
            stop='test-stop-call',
            temperature=0.6),
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,False,False,False,False,
    StrategyData(
        call=CallStrategyData(
            stop='test-stop-call',
            temperature=0.6),
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,False,False,False,False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    'Modified test content.',False,False,False,False,False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Modified test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,'test-role',False,False,False,False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='test-role',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,'test-role',False,False,False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='test-role',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,False,'test-role',False,False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='test-role'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,False,False,'modified-stop-chat',False,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='modified-stop-chat',
            temperature=0.5))),
    (StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=0.5)),
    False,False,False,False,False,1.0,
    StrategyData(
        call=False,
        chat=ChatStrategyData(
            role=Role(prompt='system',
                    input='user',
                    output='assistant'),
            prompt='Test content.',
            stop='test-stop-chat',
            temperature=1.0)))]
@pytest.mark.parametrize(['original_strategy',
                          'prompt',
                          'prompt_role','input_role','output_role',
                          'stop','temperature',
                          'ground_truth'],
                          test_method_chat_normal_cases)
def test_method_chat_normal(strategy,original_strategy,
                            prompt,
                            prompt_role,input_role,output_role,
                            stop,temperature,
                            ground_truth):
    result = strategy.chat(strategy=original_strategy,
                           prompt=prompt,
                           prompt_role=prompt_role,
                           input_role=input_role,output_role=output_role,
                           stop=stop,temperature=temperature)
    assert result == ground_truth