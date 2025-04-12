import pytest
from unittest.mock import patch,MagicMock
from llyra.local.configs import Config
from pathlib import Path

@pytest.fixture
def config():
    config = Config()
    return config

## ========================== Load Method Test ========================== ##
def test_load_default_config_file(config):
    '''Test whether method load config file from default path properly.'''
    config.load()
    attributs = ('model',
                'directory',
                'strategy',
                'gpu',
                'format',
                'ram',
                'path',)
    assert config.attributes == attributs
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_load_config_file_from_path(config):
    '''Test whether method load config form provided path properly.'''
    config.load('tests/configs/config_normal.json')
    attributs = ('model',
                'directory',
                'strategy',
                'gpu',
                'format',
                'ram',
                'path',)
    assert config.attributes == attributs
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_load_config_file_without_model_key(config):
    '''Test whether method raise exception properly when missing model key.'''
    with pytest.raises(IndexError,match='Error: Missing model file name parameter.'):
        config.load('tests/configs/config_missing_model.json')

def test_load_config_file_without_directory_key(config):
    '''Test whether method raise exception properly when missing directory key.'''
    with pytest.raises(IndexError,match='Error: Missing model file directory parameter.'):
        config.load('tests/configs/config_missing_directory.json')

def test_load_config_file_without_strategy_key(config):
    '''Test whether method show warning properly when missing strategy key.'''
    warning = 'Warning: Missing inference strategy file.\n'
    warning += '\t\t Inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_missing_strategy.json')

def test_load_config_file_without_format_key(config):
    '''Test whether method show warning properly when missing strategy key.'''
    warning = 'Warning: Missing chat format.'
    warning += '\t\t Chat inference unavailiable without manual updating'
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_missing_format.json')

## ============================= Update Method Test ============================= ##
def test_update_model_config_parameter(config):
    '''Test whether method update model config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    for possible in ['test','test.gguf']:
        config.update(model=possible,
                      directory=None,
                      strategy=None,
                      gpu=None,
                      format=None,
                      ram=None,)
        assert config.model == 'test'
        assert config.path == 'models/test.gguf'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.ram is None

def test_update_directory_config_parameter(config):
    '''Test whether method update directory config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    for possible in ['tests','tests/']:
        config.update(model=None,
                      directory=possible,
                      strategy=None,
                      gpu=None,
                      format=None,
                      ram=None,)
        assert config.directory == 'tests/'
        assert config.path == 'tests/model.gguf'
    assert config.model == 'model'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.ram is None

def test_update_strategy_config_parameter(config):
    '''Test whether method update strategy config parameter properly.
    And show warning when setting strategy to empty properly.
    '''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,
                  directory=None,
                  strategy='tests/config/strategy.json',
                  gpu=None,
                  format=None,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'tests/config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram is None
    warning = 'Warning: Missing inference strategy file.\n'
    warning += '\t\t Inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.update(model=None,
                  directory=None,
                  strategy='',
                  gpu=None,
                  format=None,
                  ram=None,)
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.strategy == ''
        assert config.gpu == False
        assert config.format == 'llama-2'
        assert config.path == 'models/model.gguf'
        assert config.ram is None

def test_update_format_config_parameter(config):
    '''Test whether method update format config parameter properly.
    And show warning when setting format to empty properly.
    '''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format='openai',
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'openai'
    assert config.path == 'models/model.gguf'
    assert config.ram is None
    warning = 'Warning: Missing chat format.'
    warning += '\t\t Chat inference unavailiable without manual updating'
    with pytest.warns(UserWarning,match=warning):
        config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format='',
                  ram=None,)
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.strategy == 'config/strategy.json'
        assert config.gpu == False
        assert config.format == ''
        assert config.path == 'models/model.gguf'
        assert config.ram is None

def test_update_gpu_config_parameter(config):
    '''Test whether method update gpu config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=True,
                  format=None,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == True
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_update_ram_config_parameter(config):
    '''Test whether method update ram config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format=None,
                  ram=False,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram == False

## ========================== Write Method Test ========================== ##
def test_writing_current_config_into_file_without_conflict(config):
    '''Test whether method write current config into file properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model='test',
                  directory='test/',
                  strategy='tests/config/strategy.json',
                  gpu=True,
                  format='openai',
                  ram=False,)
    with patch.object(Path,'exists',return_value=False):
        with patch.object(Path,'write_text') as mock_write:
            config.write()
            content = mock_write.call_args[0][0]
            assert mock_write.called
            assert '"model": "test"' in content
            assert '"directory": "test/"' in content
            assert '"strategy": "tests/config/strategy.json"' in content
            assert '"gpu": true' in content
            assert '"format": "openai"' in content
            assert '"ram": false' in content

def test_writing_current_config_into_file_with_conflict(config):
    '''Test whether methed handle condition that meets file name conflict.'''
    config.load('tests/configs/config_normal.json')
    config.update(model='test',
                  directory='test/',
                  strategy='tests/config/strategy.json',
                  gpu=True,
                  format='openai',
                  ram=False,)
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='w'):
            with patch.object(Path,'write_text') as mock_write:
                config.write()
                content = mock_write.call_args[0][0]
                assert mock_write.called
                assert '"model": "test"' in content
                assert '"directory": "test/"' in content
                assert '"strategy": "tests/config/strategy.json"' in content
                assert '"gpu": true' in content
                assert '"format": "openai"' in content
                assert '"ram": false' in content
    
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='q'):
            with patch.object(Path,'write_text') as mock_write:
                with pytest.raises(FileExistsError):
                    config.write()
                    assert not mock_write.called
