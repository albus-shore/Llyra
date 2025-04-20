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
        'create_at': log.history[0]['create_at'],
        'type': 'call',
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
    log.chat(model='model',
             prompt='You are a kind assistant.',
             role={'input':'user','output':'assistant'},
             input='hello, there!',output='hello, how can I assist you today?',
             temperature=0.6,
             strategy=None,
             keep=True)
    assert log.id == 1
    assert log.history[0] == {
        'id': 1,
        'create_at': log.history[0]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    log.chat(model='model',
             prompt='You are a kind assistant.',
             role={'input':'user','output':'assistant'},
             input='Evening!',output='Evening!',
             temperature=0.6,
             strategy=None,
             keep=True)
    assert log.id == 1
    assert log.history[0] == {
        'id': 1,
        'create_at': log.history[0]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            },
            {
            'query': 'Evening!',
            'response': 'Evening!'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    log.chat(model='model',
             prompt='You are a kind assistant.',
             role={'input':'user','output':'assistant'},
             input='hello, there!',output='hello, how can I assist you today?',
             temperature=0.6,
             strategy=None,
             keep=False)
    assert log.id == 2
    assert log.history[0] == {
        'id': 1,
        'create_at': log.history[0]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            },
            {
            'query': 'Evening!',
            'response': 'Evening!'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    assert log.history[1] == {
        'id': 2,
        'create_at': log.history[1]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    log.call(model='model',
             role={'input':'user','output':'assistant'},
             input='hello, there!',
             output='hello, how can I assist you today?',
             temperature=0.6,
             strategy=None)
    log.chat(model='model',
             prompt='You are a kind assistant.',
             role={'input':'user','output':'assistant'},
             input='Evening!',output='Evening!',
             temperature=0.6,
             strategy=None,
             keep=True)
    assert log.id == 4
    assert log.history[0] == {
        'id': 1,
        'create_at': log.history[0]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            },
            {
            'query': 'Evening!',
            'response': 'Evening!'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    assert log.history[1] == {
        'id': 2,
        'create_at': log.history[1]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    assert log.history[2] == {
        'id': 3,
        'create_at': log.history[2]['create_at'],
        'type': 'call',
        'model': 'model',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'hello, there!',
            'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    assert log.history[3] == {
        'id': 4,
        'create_at': log.history[3]['create_at'],
        'type': 'chat',
        'model': 'model',
        'prompt': 'You are a kind assistant.',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
            'query': 'Evening!',
            'response': 'Evening!'
            }],
        'temperature': 0.6,
        'strategy': None
        }
    