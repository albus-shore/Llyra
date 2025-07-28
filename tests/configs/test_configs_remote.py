import pytest
from llyra.components import RemoteConfig
from llyra.components.configs.utils import Server
from llyra.exceptions.components.configs import ConfigSectionMissingError, ConfigParameterMissingError
from llyra.exceptions.components.configs import ConfigModelNotCompatibleError

@pytest.fixture
def config():
    config = RemoteConfig()
    return config

@pytest.fixture
def loaded_config(tmp_path):
    loaded_config = RemoteConfig()
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost"
    port = 11434
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    loaded_config.load_toml(test_toml)
    return loaded_config

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(config):
    '''Test whether the class can be initialized properly.'''
    assert config.server == None
    assert config.model == None
    assert config.url == None

## ============================= `load()` Method Test ============================= ##
def test_load_toml_method(config,tmp_path):
    '''Test whether method can load and read all config parameters properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost"
    port = 11434
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load_toml(test_toml)
    # Validate loaded value
    assert config.model == 'test-model'
    assert config.server == Server('http://localhost',11434,'test/')
    assert config.url == 'http://localhost:11434/test/'

def test_load_toml_method_with_server_url_fix(config,tmp_path):
    '''Test whether method can auto fix invalid server base url parameter properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost/"
    port = 11434
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load_toml(test_toml)
    # Validate loaded value
    assert config.model == 'test-model'
    assert config.server == Server('http://localhost',11434,'test/')
    assert config.url == 'http://localhost:11434/test/'

def test_load_toml_method_with_server_endpoint_fix(config,tmp_path):
    '''Test whether method can auto fix invalid server endpoint parameter properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost"
    port = 11434
    endpoint = "test"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load_toml(test_toml)
    # Validate loaded value
    assert config.model == 'test-model'
    assert config.server == Server('http://localhost',11434,'test/')
    assert config.url == 'http://localhost:11434/test/'

def test_load_toml_method_without_model_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `model` parameter in `remote` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote.server]
    url = "http://localhost"
    port = 11434
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `model` parameter of `remote` section in `config.toml`.'):
        config.load_toml(test_toml)

def test_load_toml_method_without_server_url_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `url` parameter in `remote.server` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    port = 11434
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `url` parameter of `remote.server` section in `config.toml`.'):
        config.load_toml(test_toml)

def test_load_toml_method_without_server_port_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `port` parameter in `remote.server` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost"
    endpoint = "test/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `port` parameter of `remote.server` section in `config.toml`.'):
        config.load_toml(test_toml)        

def test_load_toml_method_without_server_endpoint_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `endpoint` parameter in `remote.server` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    [remote.server]
    url = "http://localhost"
    port = 11434
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `endpoint` parameter of `remote.server` section in `config.toml`.'):
        config.load_toml(test_toml)

def test_load_toml_method_without_server_section(config,tmp_path):
    '''Test whether method raise exception properly
    without `server` section in `remote` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    [remote]
    model = "test-model"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigSectionMissingError,
        match='remote.server'):
        config.load_toml(test_toml)

def test_load_toml_method_without_remote_section(config,tmp_path):
    '''Test whether method raise exception properly
    without `remote` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    logbase = "sqlite:///dummy_database.db"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigSectionMissingError,
        match='remote'):
        config.load_toml(test_toml)                          

## ======================== `validate_model()` Method Test ======================== ##
def test_validate_model_method(loaded_config):
    '''Test whether method can validate claiming model properly.'''
    loaded_config.validate_model('test-model')

def test_validate_model_method_with_incompatible_claiming_model(loaded_config):
    '''Test whether method raise exception properly
    when claiming model is not compatoble.'''
    with pytest.raises(ConfigModelNotCompatibleError,
        match='Config model `test-model` not compatible with model `test-model-change`.'):
        loaded_config.validate_model('test-model-change')