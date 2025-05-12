import pytest
from llyra.base import Config
from unittest.mock import patch
from pathlib import Path

@pytest.fixture
def config():
    config = Config()
    return config

@pytest.fixture
def loaded_config():
    loaded_config = Config()
    loaded_config._load('tests/configs/config_base.json')
    return loaded_config

## ========================== Load Method Test ========================== ##
def test_load_config_file_from_path(config):
    '''Test whether method load config form provided path properly.'''
    config._load('tests/configs/config_base.json')
    assert config._config == {'test': 'test'}

## ========================== Write Method Test ========================== ##
def test_writing_current_config_into_file_without_conflict(loaded_config):
    '''Test whether method write current config into file properly.'''
    test_content = {
        'test_0': 'test_0',
        'test_1': 'test_1',
        }
    with patch.object(Path,'exists',return_value=False):
        with patch.object(Path,'write_text') as mock_write:
            loaded_config._write(test_content)
            content = mock_write.call_args[0][0]
            assert mock_write.called
            assert '"test_0": "test_0"' in content
            assert '"test_1": "test_1"' in content

def test_writing_current_config_into_file_with_conflict(loaded_config):
    '''Test whether methed handle condition that meets file name conflict.'''
    test_content = {
        'test_0': 'test_0',
        'test_1': 'test_1',
        }
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='w'):
            with patch.object(Path,'write_text') as mock_write:
                loaded_config._write(test_content)
                content = mock_write.call_args[0][0]
                assert mock_write.called
                assert '"test_0": "test_0"' in content
                assert '"test_1": "test_1"' in content
    with patch.object(Path,'exists',return_value=True):
        with patch('builtins.input',return_value='q'):
            with patch.object(Path,'write_text') as mock_write:
                with pytest.raises(FileExistsError):
                    loaded_config._write(test_content)
                    assert not mock_write.called                        