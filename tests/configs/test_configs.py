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
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram == False

def test_load_config_file_from_path(config):
    '''Test whether method load config form provided path properly.'''
    config.load('tests/configs/config_normal.json')
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
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

def test_load_config_file_without_indicate_key(config):
    '''Test whether method load config without whole indicate key properly.'''
    config.load('tests/configs/config_missing_indicate.json')
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == None
    assert config.indicate['end'] == None
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_load_config_file_without_strategy_key(config):
    '''Test whether method show warning properly when missing strategy key.'''
    warning = 'Warning: Missing inference strategy file.\n'
    warning += '\t\t Inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.load('tests/configs/config_missing_strategy.json')
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_load_config_without_placeholder_key(config):
    '''Test whether mothod load config without whole placeholder key properly.'''
    config.load('tests/configs/config_missing_placeholder.json')
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == None
    assert config.placeholder['rag'] == None
    assert config.placeholder['tool'] == None
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None


## ============================= Update Method Test ============================= ##
def test_update_model_config_parameter(config):
    '''Test whether method update model config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    for possible in ['test','test.gguf']:
        config.update(model=possible,directory=None,
                      begin=None,end=None,
                      strategy=None,
                      history=None,rag=None,tool=None,
                      gpu=None,
                      ram=None,)
        assert config.model == 'test'
        assert config.path == 'models/test.gguf'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.directory == 'models/'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.ram is None

def test_update_directory_config_parameter(config):
    '''Test whether method update directory config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    for possible in ['tests','tests/']:
        config.update(model=None,directory=possible,
                      begin=None,end=None,
                      strategy=None,
                      history=None,rag=None,tool=None,
                      gpu=None,
                      ram=None,)
        assert config.directory == 'tests/'
        assert config.path == 'tests/model.gguf'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.model == 'model'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.ram is None

def test_update_indicate_config_parameter(config):
    '''Test whether method update indicate config parameter properly'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,directory=None,
                  begin='bos',end='eos',
                  strategy=None,
                  history=None,rag=None,tool=None,
                  gpu=None,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == 'bos'
    assert config.indicate['end'] == 'eos'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_update_strategy_config_parameter(config):
    '''Test whether method update strategy config parameter properly.
    And show warning when setting strategy to empty properly.
    '''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,directory=None,
                  begin=None,end=None,
                  strategy='tests/config/strategy.json',
                  history=None,rag=None,tool=None,
                  gpu=None,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'tests/config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None
    warning = 'Warning: Missing inference strategy file.\n'
    warning += '\t\t Inference unavailiable without manual updating.'
    with pytest.warns(UserWarning,match=warning):
        config.update(model=None,directory=None,
                      begin=None,end=None,
                      strategy='',
                      history=None,rag=None,tool=None,
                      gpu=None,
                      ram=None,)
        assert config.model == 'model'
        assert config.directory == 'models/'
        assert config.indicate['begin'] == '<|begin_of_sentence|>'
        assert config.indicate['end'] == '<|end_of_sentence|>'
        assert config.strategy == ''
        assert config.placeholder['history'] == '<<|History|>>'
        assert config.placeholder['rag'] == '<<|RAG|>>'
        assert config.placeholder['tool'] == '<<|Tool|>>'
        assert config.gpu == False
        assert config.path == 'models/model.gguf'
        assert config.ram is None
    
def test_update_placeholder_config_parameter(config):
    '''Test whether method update placeholder config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,directory=None,
                  begin=None,end=None,
                  strategy=None,
                  history='history',rag='rag',tool='tool',
                  gpu=None,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == 'history'
    assert config.placeholder['rag'] == 'rag'
    assert config.placeholder['tool'] == 'tool'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_update_gpu_config_parameter(config):
    '''Test whether method update gpu config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,directory=None,
                  begin=None,end=None,
                  strategy=None,
                  history=None,rag=None,tool=None,
                  gpu=True,
                  ram=None,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == True
    assert config.path == 'models/model.gguf'
    assert config.ram is None

def test_update_ram_config_parameter(config):
    '''Test whether method update ram config parameter properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model=None,directory=None,
                  begin=None,end=None,
                  strategy=None,
                  history=None,rag=None,tool=None,
                  gpu=None,
                  ram=False,)
    assert config.model == 'model'
    assert config.directory == 'models/'
    assert config.indicate['begin'] == '<|begin_of_sentence|>'
    assert config.indicate['end'] == '<|end_of_sentence|>'
    assert config.strategy == 'config/strategy.json'
    assert config.placeholder['history'] == '<<|History|>>'
    assert config.placeholder['rag'] == '<<|RAG|>>'
    assert config.placeholder['tool'] == '<<|Tool|>>'
    assert config.gpu == False
    assert config.path == 'models/model.gguf'
    assert config.ram == False

## ========================== Write Method Test ========================== ##
def test_writing_current_config_into_file_without_conflict(config):
    '''Test whether method write current config into file properly.'''
    config.load('tests/configs/config_normal.json')
    config.update(model='test',directory='test/',
                  begin='bos',end='eos',
                  strategy='tests/config/strategy.json',
                  history='history',rag='rag',tool='tool',
                  gpu=True,
                  ram=False,)
    with patch.object(Path,'exists',return_value=False):
        with patch.object(Path,'write_text') as mock_write:
            config.write()
            content = mock_write.call_args[0][0]
            assert mock_write.called
            assert '"model": "test"' in content
            assert '"directory": "test/"' in content
            assert '"indicate": {"begin": "bos", "end": "eos"}' in content
            assert '"strategy": "tests/config/strategy.json"' in content
            assert '"placeholder": {"history": "history", "rag": "rag", "tool": "tool"}' in content
            assert '"gpu": true' in content
            assert '"ram": false' in content

def test_writing_current_config_into_file_with_conflict(config):
    '''Test whether methed handle condition that meets file name conflict.'''
    config.load('tests/configs/config_normal.json')
    config.update(model='test',directory='test/',
                  begin='bos',end='eos',
                  strategy='tests/config/strategy.json',
                  history='history',rag='rag',tool='tool',
                  gpu=True,
                  ram=False,)
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='w'):
            with patch.object(Path,'write_text') as mock_write:
                config.write()
                content = mock_write.call_args[0][0]
                assert mock_write.called
                assert '"model": "test"' in content
                assert '"directory": "test/"' in content
                assert '"indicate": {"begin": "bos", "end": "eos"}' in content
                assert '"strategy": "tests/config/strategy.json"' in content
                assert '"placeholder": {"history": "history", "rag": "rag", "tool": "tool"}' in content
                assert '"gpu": true' in content
                assert '"ram": false' in content
    
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='q'):
            with patch.object(Path,'write_text') as mock_write:
                with pytest.raises(FileExistsError):
                    config.write()
                    assert not mock_write.called
