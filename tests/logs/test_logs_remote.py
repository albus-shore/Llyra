import pytest
from llyra.remote.logs import LogRemote

@pytest.fixture
def log():
    log = LogRemote()
    return log

## ========================== Record Methods Test ========================== ##
def test_call_method(log):
    '''Test whether the method can record inference history properly.'''
    log.call(model='model',
             input='hello, there!',
             output='hello, how can I assist you today?')
    record = log.get(0)
    assert log.id == 1
    assert record == {
        'id': 0,
        'type': 'call',
        'model': 'model',
        'prompt': None,
        'role': None,
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'create_at': log._history[0].create_at,
        }
    
def test_chat_method(log):
    '''Test whether the method can record inference history properly.'''
    prompt = 'This is for test.'
    role = {
        'prompt': 'system',
        'input': 'user',
        'output': 'assistant',
        }
    log.chat(model='model',
             prompt=prompt,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             keep=True)
    record = log.get(0)
    assert log.id == 1
    assert record == {
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }    