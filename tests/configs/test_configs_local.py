import pytest
from llyra.components import LocalConfig
from llyra.components.configs.utils import Model
from llyra.errors.components.configs import ConfigSectionMissingError, ConfigParameterMissingError

@pytest.fixture
def config():
    config = LocalConfig()
    return config

@pytest.fixture
def loaded_config(tmp_path):
    loaded_config = LocalConfig()
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Load test config content
    loaded_config.load(test_toml)
    return loaded_config

## =========================== `__init__()` Method Test =========================== ##
def test_initialize_method(config):
    '''Test whether the class can be initialized properly.'''
    assert config.model == None
    assert config.format == None
    assert config.gpu == None
    assert config.ram == None
    assert config.path == None

## ============================= `load()` Method Test ============================= ##
def test_load_method(config,tmp_path):
    '''Test whether method can load and read all config parameters properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load(test_toml)
    # Validate loaded value
    assert config.model == Model('test-model','dummy_directory/','.gguf')
    assert config.format == "test-format"
    assert config.gpu == True
    assert config.ram == False
    assert config.path == 'dummy_directory/test-model.gguf'

def test_load_method_with_model_name_fix(config,tmp_path):
    '''Test whether method can auto fix invalid model name parameter properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model.gguf"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load(test_toml)
    # Validate loaded value
    assert config.model == Model('test-model','dummy_directory/','.gguf')
    assert config.path == 'dummy_directory/test-model.gguf'

def test_load_method_with_model_directory_fix(config,tmp_path):
    '''Test whether method can auto fix invalid model directory parameter properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load(test_toml)
    # Validate loaded value
    assert config.model == Model('test-model','dummy_directory/','.gguf')
    assert config.path == 'dummy_directory/test-model.gguf'    

def test_load_method_with_model_suffix_fix(config,tmp_path):
    '''Test whether method can auto fix invalid model suffix parameter properly.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = "gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    config.load(test_toml)
    # Validate loaded value
    assert config.model == Model('test-model','dummy_directory/','.gguf')
    assert config.path == 'dummy_directory/test-model.gguf'        

def test_load_method_with_format_fallback(config,tmp_path):
    '''Test whether method auto fallback to `None` and rasie warning 
    when missing `format` parameter.'''
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    warns_message = 'Missing `format` parameter of `local` section in `config.toml`'
    warns_message += ' , auto-fallback to `None`.'
    with pytest.warns(RuntimeWarning,match=warns_message):
        config.load(test_toml)
    # Validate loaded value
    assert config.format == None

def test_load_method_with_gpu_fallback(config,tmp_path):
    '''Test whether method auto fallback to `False` and rasie warning 
    when missing `gpu` parameter.'''
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    warns_message = 'Missing `gpu` parameter of `local` section in `config.toml`'
    warns_message += ' , auto-fallback to `False`.'
    with pytest.warns(RuntimeWarning,match=warns_message):
        config.load(test_toml)
    # Validate loaded value
    assert config.gpu == False

def test_load_method_with_ram_fallback(config,tmp_path):
    '''Test whether method auto fallback to `False` and rasie warning 
    when missing `ram` parameter.'''
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    warns_message = 'Missing `ram` parameter of `local` section in `config.toml`'
    warns_message += ' , auto-fallback to `False`.'
    with pytest.warns(RuntimeWarning,match=warns_message):
        config.load(test_toml)
    # Validate loaded value
    assert config.ram == False

def test_load_method_without_model_name_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `name` parameter in `local.model` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    directory = "dummy_directory/"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `name` parameter of `local.model` section in `config.toml`.'):
        config.load(test_toml)

def test_load_method_without_model_directory_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `directory` parameter in `local.model` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    suffix = ".gguf"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `directory` parameter of `local.model` section in `config.toml`.'):
        config.load(test_toml)        

def test_load_method_without_model_suffix_parameter(config,tmp_path):
    '''Test whether method raise exception properly
    without `suffix` parameter in `local.model` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    [local.model]
    name = "test-model"
    directory = "dummy_directory/"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigParameterMissingError,
        match='Missing `suffix` parameter of `local.model` section in `config.toml`.'):
        config.load(test_toml)   

def test_load_method_without_model_section(config,tmp_path):
    '''Test whether method raise exception properly
    without `model` section in `local` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    [local]
    format = "test-format"
    gpu = true
    ram = false
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigSectionMissingError,
        match='local.model'):
        config.load(test_toml)               

def test_load_method_without_local_section(config,tmp_path):
    '''Test whether method raise exception properly
    without `local` section.'''
    # Set test config file
    content = '''
    [global]
    strategy = "dummy_directory/dummy_strategy.toml"
    '''
    test_toml = tmp_path / 'test.toml'
    test_toml.write_text(content)
    # Execute config load
    with pytest.raises(ConfigSectionMissingError,
        match='local'):
        config.load(test_toml)            

## ============================ `update()` Method Test ============================ ##
def test_update_method(loaded_config):
    '''Test whether method can update not key config parameter properly.'''
    # Execute config update        
    loaded_config.update(None,False,True)
    # Validate updated value
    assert loaded_config.format == None
    assert loaded_config.gpu == False
    assert loaded_config.ram == True

def test_update_method_ignoring_format_parameters(loaded_config):    
    '''Test whether method can ignore `format` parameter and
    update other not key config parameter at the same time properly.'''
    # Execute config update ignoring format        
    loaded_config.update('',False,True)
    # Validate updated value
    assert loaded_config.format == 'test-format'
    assert loaded_config.gpu == False
    assert loaded_config.ram == True

def test_update_method_ignoring_gpu_parameters(loaded_config):    
    '''Test whether method can ignore `gpu` parameter and
    update other not key config parameter at the same time properly.'''
    # Execute config update ignoring format        
    loaded_config.update(None,None,True)
    # Validate updated value
    assert loaded_config.format == None
    assert loaded_config.gpu == True
    assert loaded_config.ram == True    

def test_update_method_ignoring_ram_parameters(loaded_config):    
    '''Test whether method can ignore `gpu` parameter and
    update other not key config parameter at the same time properly.'''
    # Execute config update ignoring format        
    loaded_config.update(None,False,None)
    # Validate updated value
    assert loaded_config.format == None
    assert loaded_config.gpu == False
    assert loaded_config.ram == False        