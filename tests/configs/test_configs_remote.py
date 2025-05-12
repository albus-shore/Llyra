import pytest
from unittest.mock import patch
from llyra.remote.configs import ConfigRemote
from pathlib import Path

@pytest.fixture
def config():
    config = ConfigRemote()
    return config

@pytest.fixture
def loaded_config():
    loaded_config = ConfigRemote()
    loaded_config.load('tests/configs/config_remote.json')
    return loaded_config

## ========================== Load Method Test ========================== ##
def test_load_default_config_file(config):
    '''Test whether method load config file from default path properly.'''
    config.load()
    assert config.url == 'http://localhost:11434/'
    assert config.endpoint == 'api/'
    assert config.model == 'llama-2'
    assert config.strategy == 'config/config-remote.json'
    assert config.stream == False

def test_load_config_file_from_path(config):
    '''Test whether method load config from provided path properly.'''
    config.load('tests/configs/config_remote.json')
    assert config.url == 'http://localhost:11434/'
    assert config.endpoint == 'api/'
    assert config.model == 'llama-2'
    assert config.strategy == 'config/config-remote.json'
    assert config.stream == False

def test_load_config_file_without_url_key(config):
    '''Test whether method raise exception properly when missing url key.'''
    with pytest.raises(IndexError,match='Error: Missing base URL parameter.'):
        config.load('tests/configs/config_without_url.json')

def test_load_config_file_without_endpoint_key(config):
    '''Test whether method raise exception properly when missing endpoint key.'''
    with pytest.raises(IndexError,match='Error: Missing service endpoint parameter.'):
        config.load('tests/configs/config_without_endpoint.json')

def test_load_config_file_without_model_key(config):
    '''Test whether method show warning properly when missing model key.'''
    warning = 'Warning: Missing instructed model for inference.\n'
    warning += '\t\t All inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_without_model.json')
        assert config.url == 'http://localhost:11434/'
        assert config.endpoint == 'api/'
        assert config.model == None
        assert config.strategy == 'config/config-remote.json'
        assert config.stream == False

def test_load_config_file_without_strategy_key(config):
    '''Test whether method show warning properly when missing strategy key.'''
    warning = 'Warning: Missing inference file.\n'
    warning += '\t\t Chat inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_without_strategy.json')
        assert config.url == 'http://localhost:11434/'
        assert config.endpoint == 'api/'
        assert config.model == 'llama-2'
        assert config.strategy == None
        assert config.stream == False

def test_load_config_file_without_stream_key(config):
    '''Test whether method load defualt value when missing stream key.'''
    config.load('tests/configs/config_without_stream.json')
    assert config.url == 'http://localhost:11434/'
    assert config.endpoint == 'api/'
    assert config.model == 'llama-2'
    assert config.strategy == 'config/config-remote.json'
    assert config.stream == False

## ============================= Update Method Test ============================= ##
def test_update_url_config_parameter(loaded_config):
    '''Test whether method update url config parameter properly.'''
    for possible in ['test','test/']:
        loaded_config.update(url=possible,
                             endpoint=None,
                             model=None,
                             strategy=None,
                             stream=None,)
        assert loaded_config.url == 'test/'
    assert loaded_config.endpoint == 'api/'
    assert loaded_config.model == 'llama-2'
    assert loaded_config.strategy == 'config/config-remote.json'
    assert loaded_config.stream == False    

def test_update_endpoint_config_parameter(loaded_config):
    '''Test whether method update endpoint config parameter properly.'''
    for possible in ['test','test/']:
        loaded_config.update(url=None,
                             endpoint=possible,
                             model=None,
                             strategy=None,
                             stream=None,)
        assert loaded_config.endpoint == 'test/'
    assert loaded_config.url == 'http://localhost:11434/'
    assert loaded_config.model == 'llama-2'
    assert loaded_config.strategy == 'config/config-remote.json'
    assert loaded_config.stream == False

def test_update_model_config_parameter(loaded_config):
    '''Test whether method update model config parameter properly.
    And show warning when setting model to empty.
    '''
    loaded_config.update(url=None,
                         endpoint=None,
                         model='test',
                         strategy=None,
                         stream=None,)
    assert loaded_config.url == 'http://localhost:11434/'
    assert loaded_config.endpoint == 'api/'
    assert loaded_config.model == 'test'
    assert loaded_config.strategy == 'config/config-remote.json'
    assert loaded_config.stream == False 
    warning = 'Warning: Missing instructed model for inference.\n'
    warning += '\t\t All inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        loaded_config.update(url=None,
                             endpoint=None,
                             model='',
                             strategy=None,
                             stream=None,)
        assert loaded_config.url == 'http://localhost:11434/'
        assert loaded_config.endpoint == 'api/'
        assert loaded_config.model == ''
        assert loaded_config.strategy == 'config/config-remote.json'
        assert loaded_config.stream == False

def test_update_strategy_config_parameter(loaded_config):
    '''Test whether method update strategy config parameter properly.
    And show warning when setting strategy to empty.
    '''
    loaded_config.update(url=None,
                         endpoint=None,
                         model=None,
                         strategy='tests/configs/strategy.json',
                         stream=None,)
    assert loaded_config.url == 'http://localhost:11434/'
    assert loaded_config.endpoint == 'api/'
    assert loaded_config.model == 'llama-2'
    assert loaded_config.strategy == 'tests/configs/strategy.json'
    assert loaded_config.stream == False
    warning = 'Warning: Missing inference file.\n'
    warning += '\t\t Chat inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        loaded_config.update(url=None,
                         endpoint=None,
                         model=None,
                         strategy='',
                         stream=None,)
        assert loaded_config.url == 'http://localhost:11434/'
        assert loaded_config.endpoint == 'api/'
        assert loaded_config.model == 'llama-2'
        assert loaded_config.strategy == ''
        assert loaded_config.stream == False

def test_update_stream_config_parameter(loaded_config):
    '''Test whether method update stream config parameter properly.
    And show warning when setting stream to empty.
    '''
    loaded_config.update(url=None,
                         endpoint=None,
                         model=None,
                         strategy=None,
                         stream=True,)
    assert loaded_config.url == 'http://localhost:11434/'
    assert loaded_config.endpoint == 'api/'
    assert loaded_config.model == 'llama-2'
    assert loaded_config.strategy == 'config/config-remote.json'
    assert loaded_config.stream == True

## ========================== Write Method Test ========================== ##
def test_writing_current_config_into_file(loaded_config):
    '''Test whether method write current config into file properly.'''
    loaded_config.update(url='test',
                         endpoint='test',
                         model='test',
                         strategy='tests/configs/strategy.json',
                         stream=True,)
    with patch.object(Path,'exists',return_value=False):
        with patch.object(Path,'write_text') as mock_write:
            loaded_config.write()
            content = mock_write.call_args[0][0]
            assert mock_write.called
            assert '"url": "test/"' in content
            assert '"endpoint": "test/"' in content
            assert '"model": "test"' in content
            assert '"strategy": "tests/configs/strategy.json"' in content
            assert '"stream": true' in content