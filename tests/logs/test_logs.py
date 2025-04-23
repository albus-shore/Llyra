import pytest
from llyra.local.logs import Log

@pytest.fixture
def log():
    log = Log()
    return log

## ========================== Initialize Method Test ========================== ##
def test_initialize_method(log):
    '''Test whether the class can be initialized properly.'''
    assert log.id == 0
    assert log.history == []

## ========================== Record Methods Test ========================== ##
def test_call_method(log):
    '''Test whether the method can record inference history properly.'''
    log.call(model='model',
             role={'input':'user','output':'assistant'},
             input='hello, there!',
             output='hello, how can I assist you today?',
             temperature=0.6,
             strategy=None)
    assert log.id == 1
    assert log.history[0] == {
        'id': 1,
        'type': 'call',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
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
             temperature=0.6,
             strategy='strategy.json',
             keep=True)
    assert log.id == 1
    assert log.history == [{
        'id': 1,
        'type': 'chat',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        }]
    log.chat(model='model',
             prompt=prompt,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             strategy='strategy.json',
             keep=True)
    assert log.id == 1
    assert log.history == [{
        'id': 1,
        'type': 'chat',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        }]
    log.chat(model='model',
             prompt=prompt,
             role=role,
             input='Good day!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             strategy='strategy.json',
             keep=False)
    assert log.id == 2
    assert log.history == [{
        'id': 1,
        'type': 'chat',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        },{
        'id': 2,
        'type': 'chat',
        'create_at': log.history[1]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        }]
    log.call(model='model',
             role={'input':'user','output':'assistant'},
             input='hello, there!',
             output='hello, how can I assist you today?',
             temperature=0.6,
             strategy=None)
    assert log.id == 3
    assert log.history == [{
        'id': 1,
        'type': 'chat',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        },{
        'id': 2,
        'type': 'chat',
        'create_at': log.history[1]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        },{
        'id': 3,
        'type': 'call',
        'create_at': log.history[2]['create_at'],
        'model': 'model',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }]
    log.chat(model='model',
             prompt=prompt,
             role=role,
             input='Hello, there!',output='Greeting, how can I assist you today?',
             temperature=0.6,
             strategy='strategy.json',
             keep=True)
    assert log.id == 4
    assert log.history == [{
        'id': 1,
        'type': 'chat',
        'create_at': log.history[0]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'},
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        },{
        'id': 2,
        'type': 'chat',
        'create_at': log.history[1]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Good day!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        },{
        'id': 3,
        'type': 'call',
        'create_at': log.history[2]['create_at'],
        'model': 'model',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        },{
        'id': 4,
        'type': 'chat',
        'create_at': log.history[3]['create_at'],
        'model': 'model',
        'prompt': prompt,
        'role': role,
        'iteration': [
            {'query': 'Hello, there!', 'response': 'Greeting, how can I assist you today?'}
            ],
        'temperature': 0.6,
        'strategy': 'strategy.json'
        }]
