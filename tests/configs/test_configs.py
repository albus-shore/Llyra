import pytest
from llyra.local.configs import Config

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