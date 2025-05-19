import pytest
from llyra.base.logs import Log
@pytest.fixture
def log():
    log = Log()
    return log

## ========================== Initialize Method Test ========================== ##
def test_initialize_method(log):
    '''Test whether the class can be initialized properly.'''
    assert log.id == 0
    assert log._history == []

## ========================== Record Methods Test ========================== ##
def test_call_method(log):
    '''Test whether the method can record inference history properly.'''
    log._call(model='model',
             role={'input':'user','output':'assistant'},
             input='hello, there!',
             output='hello, how can I assist you today?')
    record = log.get(0)
    assert log.id == 1
    assert record == {
        'id': 0,
        'type': 'call',
        'model': 'model',
        'prompt': None,
        'role': {'input':'user','output':'assistant'},
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
    log._chat(model='model',
             prompt=prompt,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             keep=True)
    record = log.get(-1)
    assert log.id == 1
    assert record == [{
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }]
    log._chat(model='model',
             prompt=prompt,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             keep=True)
    record = log.get(-1)
    assert log.id == 1
    assert record == [{
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }]
    log._chat(model='model',
             prompt=prompt,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             keep=False)
    record = log.get(-1)
    assert log.id == 2
    assert record == [{
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        },{
        'id': 1,
        'type': 'chat',
        'create_at': log._history[1].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }]
    log._call(model='model',
             role={'input':'user','output':'assistant'},
             input='hello, there!',
             output='hello, how can I assist you today?',)
    record = log.get(-1)
    assert log.id == 3
    assert record == [{
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        },{
        'id': 1,
        'type': 'chat',
        'create_at': log._history[1].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        },{
        'id': 2,
        'type': 'call',
        'create_at': log._history[2].create_at,
        'model': 'model',
        'prompt': None,
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        }]
    log._chat(model='model',
             prompt=prompt,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             keep=True)
    record = log.get(-1)
    assert log.id == 4
    assert record == [{
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        },{
        'id': 1,
        'type': 'chat',
        'create_at': log._history[1].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        },{
        'id': 2,
        'type': 'call',
        'create_at': log._history[2].create_at,
        'model': 'model',
        'prompt': None,
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        },{
        'id': 3,
        'type': 'chat',
        'create_at': log._history[3].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }]
    record = log.get(0)
    assert record == {
        'id': 0,
        'type': 'chat',
        'create_at': log._history[0].create_at,
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        }