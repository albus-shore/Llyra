import pytest
from unittest.mock import patch,MagicMock
from llyra.local.configs import ConfigLocal
from pathlib import Path

@pytest.fixture
def config():
    config = ConfigLocal()
    return config

@pytest.fixture
def loaded_config():
    loaded_config = ConfigLocal()
    loaded_config.load('tests/configs/config_normal.json')
    return loaded_config

## ========================== Load Method Test ========================== ##
def test_load_default_config_file(config):
    '''Test whether method load config file from default path properly.'''
    warning = 'Warning: Missing chat format.\n'
    warning += '\t\t Chat inference may unavailiable '
    warning += "when chat format not contain in model's metadate "
    warning += "or not manual updating."
    with pytest.warns(UserWarning,match=warning):
        config.load()
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.strategy == 'config/strategy.json'
        assert config.gpu == False
        assert config.format == None
        assert config.path == 'models/model.gguf'
        assert config.ram is False

def test_load_config_file_from_path(config):
    '''Test whether method load config form provided path properly.'''
    config.load('tests/configs/config_normal.json')
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.gpu == False
    assert config.format == 'llama-2'
    assert config.path == 'models/model.gguf'
    assert config.ram is False

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
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.strategy == None
        assert config.gpu == False
        assert config.format == 'llama-2'
        assert config.path == 'models/model.gguf'
        assert config.ram is False

def test_load_config_file_without_format_key(config):
    '''Test whether method show warning properly when missing strategy key.'''
    warning = 'Warning: Missing chat format.\n'
    warning += '\t\t Chat inference may unavailiable '
    warning += "when chat format not contain in model's metadate "
    warning += "or not manual updating."
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_missing_format.json')
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.strategy == 'config/strategy.json'
        assert config.gpu == False
        assert config.format == None
        assert config.path == 'models/model.gguf'
        assert config.ram is False

## ============================= Update Method Test ============================= ##
def test_update_model_config_parameter(loaded_config):
    '''Test whether method update model config parameter properly.'''
    for possible in ['test','test.gguf']:
        loaded_config.update(model=possible,
                      directory=None,
                      strategy=None,
                      gpu=None,
                      format=None,
                      ram=None,)
        assert loaded_config.model == 'test'
        assert loaded_config.path == 'models/test.gguf'
    assert loaded_config.directory == 'models/'
    assert loaded_config.strategy == 'config/strategy.json'
    assert loaded_config.gpu == False
    assert loaded_config.format == 'llama-2'
    assert loaded_config.ram == False

def test_update_directory_config_parameter(loaded_config):
    '''Test whether method update directory config parameter properly.'''
    for possible in ['tests','tests/']:
        loaded_config.update(model=None,
                      directory=possible,
                      strategy=None,
                      gpu=None,
                      format=None,
                      ram=None,)
        assert loaded_config.directory == 'tests/'
        assert loaded_config.path == 'tests/model.gguf'
    assert loaded_config.model == 'model'
    assert loaded_config.strategy == 'config/strategy.json'
    assert loaded_config.gpu == False
    assert loaded_config.format == 'llama-2'
    assert loaded_config.ram == False

def test_update_strategy_config_parameter(loaded_config):
    '''Test whether method update strategy config parameter properly.
    And show warning when setting strategy to empty properly.
    '''
    loaded_config.update(model=None,
                  directory=None,
                  strategy='tests/config/strategy.json',
                  gpu=None,
                  format=None,
                  ram=None,)
    assert loaded_config.model == 'model'
    assert loaded_config.directory == 'models/'
    assert loaded_config.strategy == 'tests/config/strategy.json'
    assert loaded_config.gpu == False
    assert loaded_config.format == 'llama-2'
    assert loaded_config.path == 'models/model.gguf'
    assert loaded_config.ram == False
    warning = 'Warning: Missing inference strategy file.\n'
    warning += '\t\t Inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        loaded_config.update(model=None,
                  directory=None,
                  strategy='',
                  gpu=None,
                  format=None,
                  ram=None,)
        assert loaded_config.model == 'model'
        assert loaded_config.directory == 'models/'
        assert loaded_config.strategy == ''
        assert loaded_config.gpu == False
        assert loaded_config.format == 'llama-2'
        assert loaded_config.path == 'models/model.gguf'
        assert loaded_config.ram == False

def test_update_format_config_parameter(loaded_config):
    '''Test whether method update format config parameter properly.
    And show warning when setting format to empty properly.
    '''
    loaded_config.load('tests/configs/config_normal.json')
    loaded_config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format='openai',
                  ram=None,)
    assert loaded_config.model == 'model'
    assert loaded_config.directory == 'models/'
    assert loaded_config.strategy == 'config/strategy.json'
    assert loaded_config.gpu == False
    assert loaded_config.format == 'openai'
    assert loaded_config.path == 'models/model.gguf'
    assert loaded_config.ram == False
    warning = 'Warning: Missing chat format.\n'
    warning += '\t\t Chat inference may unavailiable '
    warning += "when chat format not contain in model's metadate "
    warning += "or not manual updating."
    with pytest.warns(UserWarning,match=warning):
        loaded_config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format='',
                  ram=None,)
        assert loaded_config.model == 'model'
        assert loaded_config.directory == 'models/'
        assert loaded_config.strategy == 'config/strategy.json'
        assert loaded_config.gpu == False
        assert loaded_config.format == ''
        assert loaded_config.path == 'models/model.gguf'
        assert loaded_config.ram == False

def test_update_gpu_config_parameter(loaded_config):
    '''Test whether method update gpu config parameter properly.'''
    loaded_config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=True,
                  format=None,
                  ram=None,)
    assert loaded_config.model == 'model'
    assert loaded_config.directory == 'models/'
    assert loaded_config.strategy == 'config/strategy.json'
    assert loaded_config.gpu == True
    assert loaded_config.format == 'llama-2'
    assert loaded_config.path == 'models/model.gguf'
    assert loaded_config.ram == False

def test_update_ram_config_parameter(loaded_config):
    '''Test whether method update ram config parameter properly.'''
    loaded_config.load('tests/configs/config_normal.json')
    loaded_config.update(model=None,
                  directory=None,
                  strategy=None,
                  gpu=None,
                  format=None,
                  ram=True,)
    assert loaded_config.model == 'model'
    assert loaded_config.directory == 'models/'
    assert loaded_config.strategy == 'config/strategy.json'
    assert loaded_config.gpu == False
    assert loaded_config.format == 'llama-2'
    assert loaded_config.path == 'models/model.gguf'
    assert loaded_config.ram == True

## ========================== Write Method Test ========================== ##
def test_writing_current_config_into_file_without_conflict(loaded_config):
    '''Test whether method write current config into file properly.'''
    loaded_config.update(model='test',
                  directory='test/',
                  strategy='tests/config/strategy.json',
                  gpu=True,
                  format='openai',
                  ram=False,)
    with patch.object(Path,'exists',return_value=False):
        with patch.object(Path,'write_text') as mock_write:
            loaded_config.write()
            content = mock_write.call_args[0][0]
            assert mock_write.called
            assert '"model": "test"' in content
            assert '"directory": "test/"' in content
            assert '"strategy": "tests/config/strategy.json"' in content
            assert '"gpu": true' in content
            assert '"format": "openai"' in content
            assert '"ram": false' in content

def test_writing_current_config_into_file_with_conflict(loaded_config):
    '''Test whether methed handle condition that meets file name conflict.'''
    loaded_config.update(model='test',
                  directory='test/',
                  strategy='tests/config/strategy.json',
                  gpu=True,
                  format='openai',
                  ram=False,)
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='w'):
            with patch.object(Path,'write_text') as mock_write:
                loaded_config.write()
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
                    loaded_config.write()
                    assert not mock_write.called
