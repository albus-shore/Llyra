import pytest
from llyra.components.configs.basic import Config
from llyra.errors.configs import ConfigParameterMissingError, ConfigSectionMissingError
from pathlib import Path

@pytest.fixture
def config():
    config = Config()
    return config

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(config):
    '''Test whether the class can be initialized properly.'''
    assert config._path == Path('configs/config.toml')
    assert config.strategy == None
    assert config._content == None

## ============================= `load()` Method Test ============================= ##
def test_load_config_file_from_default_path(config):
    '''Test whether method load config from default properly.'''
    # Execute config load
    config._load(None)
    # Validate loaded value
    assert config._path == Path('configs/config.toml')
    assert config.strategy == Path("configs/strategy.toml")
    assert config._content == {
        'global': {
            'strategy': "configs/strategy.toml",
            },
        'local': {
            'model': {
                'name': 'Distill-Llama-8B',
                'directory': 'models/',
                'suffix': '.gguf',
                },
            'format': 'llama-2',
            'gpu': True,
            'ram': False,
            },
        'remote':{
            'server': {
                'url': 'http://localhost',
                'port': 11434,
                'endpoint': 'api/',
                },
            'model': 'llama-2',
            }
    }

def test_load_config_file_from_Path_object(config,tmp_path):
    '''Test whether method load config from provided Path object properly.'''
    # Set test path
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [test]
    test_parameter = "test_parameter_content"
    [test.test]
    test_parameter = "test_parameter_content"
    '''
    test_toml = tmp_path / 'test_toml'
    test_toml.write_text(content,encoding='utf-8')
    # Execute config load
    config._load(test_toml)
    # Validate loaded value
    assert config._path == test_toml
    assert config.strategy == Path("dummy_directory/dummy_strategy.toml")
    assert config._content == {
        'global': {
            'strategy': "dummy_directory/dummy_strategy.toml"
        },
        'test': {
            'test_parameter': "test_parameter_content",
            'test': {
                'test_parameter': "test_parameter_content"
            }
        }
    }

def test_load_config_file_from_string_path(config,tmp_path):
    '''Test whether method load config from provided string path properly.'''
    # Set test path
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [test]
    test_parameter = "test_parameter_content"
    [test.test]
    test_parameter = "test_parameter_content"
    '''
    test_toml = tmp_path / 'test_toml'
    test_toml.write_text(content,encoding='utf-8')
    # Execute config load
    config._load(str(test_toml))
    # Validate loaded value
    assert config._path == test_toml
    assert config.strategy == Path("dummy_directory/dummy_strategy.toml")
    assert config._content == {
        'global': {
            'strategy': "dummy_directory/dummy_strategy.toml"
        },
        'test': {
            'test_parameter': "test_parameter_content",
            'test': {
                'test_parameter': "test_parameter_content"
            }
        }
    }

def test_load_config_file_when_missing_file(config):
    '''Test whether method raise exception properly
    when load config from default path and missing it.'''
    # Override default path
    config._path = Path('config/config.toml')
    # Execute config load
    with pytest.raises(FileNotFoundError,match='Missing config file.'):
        config._load(None)

def test_load_config_file_from_error_path(config):
    '''Test whether method raise exception properly
    when load config from error custom path.'''
    # Set error path
    path = Path('config/config.toml')
    # Execute config load
    with pytest.raises(FileNotFoundError,
                       match='Config file not found in provided path.'):
        config._load(path)

def test_load_config_file_without_global_section(config,tmp_path):
    '''Test whether method raise exception properly
    without `global` section.'''
    # Set test path
    content = '''
    [test]
    test_parameter = "test_parameter_content"
    [test.test]
    test_parameter = "test_parameter_content"
    '''
    test_toml = tmp_path / 'test_toml'
    test_toml.write_text(content,encoding='utf-8')
    # Execute config load
    with pytest.raises(ConfigSectionMissingError,
        match='Missing `global` section in `config.toml`.' ):
        config._load(test_toml)

def test_load_config_file_without_strategy_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `strategy` parameter.'''
    # Set test path
    content = '''
    [global]
    [test]
    test_parameter = "test_parameter_content"
    [test.test]
    test_parameter = "test_parameter_content"
    '''
    test_toml = tmp_path / 'test_toml'
    test_toml.write_text(content,encoding='utf-8')
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `strategy` parameter of `global` section in `config.toml`.'):
        config._load(test_toml)