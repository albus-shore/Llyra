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
        'model': 'model',
        'role': {'input':'user','output':'assistant'},
        'iteration': [{
        'query': 'hello, there!',
        'response': 'hello, how can I assist you today?'
            }],
        'temperature': 0.6,
        'strategy': None
        }