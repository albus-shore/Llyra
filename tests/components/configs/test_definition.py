import pytest
from llyra.components.configs import Config
from llyra.data.components import ConfigData
from llyra.data.components.configs.utils.classes import LocalConfigData, \
    RemoteConfigData
from llyra.exceptions.components.configs import ConfigParameterMissingError, \
    ConfigSectionMissingError, ConfigUnsupportedInferenceModeError
from pathlib import Path

## ============================ Test original instance ============================ ##
@pytest.fixture
def original_config():
    return Config()

## ========================== Test original `load` method ========================== ##
def test_method_load_original_local(original_config):
    test_result = original_config.load('Local')
    ground_truth = ConfigData(model='Distill-Llama-8B',
                              strategy=Path('configs/strategy.toml'),
                              local=LocalConfigData(
                                  model=Path('models/Distill-Llama-8B.gguf'),
                                  format='llama-2',
                                  gpu=True,
                                  ram=False),
                                  remote=False)
    assert test_result == ground_truth

def test_method_load_original_remote(original_config):
    test_result = original_config.load('Remote')
    ground_truth = ConfigData(model='llama-2',
                              strategy=Path('configs/strategy.toml'),
                              local=False,
                              remote=RemoteConfigData(
                                  model='llama-2',
                                  url='http://localhost:11434/api/'))
    assert test_result == ground_truth

## =============================== Test `set` method =============================== ##
def test_method_set_with_path_instance(original_config):
    original_config.set(Path('test/test.toml'))
    assert original_config.path == Path('test/test.toml')

def test_method_set_with_str(original_config):
    original_config.set('test/test.toml')
    assert original_config.path == Path('test/test.toml')

## ================================= Test instance ================================= ##
@pytest.fixture
def config(tmp_path):
    # Build test instance
    config = Config()
    # Build test config file path
    test_path = tmp_path / 'test.toml'
    # Set test config file path
    config.set(test_path)
    # Return test instance
    return config

## ============================== Test `load` method ============================== ##
def test_method_load_with_worry_path(config):
    with pytest.raises(FileNotFoundError,match='Configuration File Not Found'):
        config.load('Local')

test_method_load_normal_cases = [
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Local',
     ConfigData(model='test-model-local',strategy=Path('test/strategy.toml'),local=LocalConfigData(model=Path('models/test-model-local.gguf'),format='test-format',gpu=True,ram=False),remote=False)),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Local',
     ConfigData(model='test-model-local',strategy=Path('test/strategy.toml'),local=LocalConfigData(model=Path('models/test-model-local.gguf'),format='test-format',gpu=True,ram=False),remote=False)),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Remote',
     ConfigData(model='test-model-remote',strategy=Path('test/strategy.toml'),local=False,remote=RemoteConfigData(model='test-model-remote',url='http://localhost:11434/api/'))),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Remote',
     ConfigData(model='test-model-remote',strategy=Path('test/strategy.toml'),local=False,remote=RemoteConfigData(model='test-model-remote',url='http://localhost:11434/api/'))),
    ]
@pytest.mark.parametrize(['test_config','test_mode','ground_truth'],
                         test_method_load_normal_cases)
def test_method_load_normal(config,tmp_path,test_config,test_mode,ground_truth):
    # Build test config file
    test_path = tmp_path / 'test.toml'
    test_path.write_text(test_config)
    # Check load result
    result = config.load(test_mode)
    assert result == ground_truth

test_method_load_raise_cases = [
    ('[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Local',
     ConfigSectionMissingError,
     'Missing `global` section in config file.'),
    ('[global]\n\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Local',
     ConfigParameterMissingError,
     'Missing `strategy` parameter in `global` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Other',
     ConfigUnsupportedInferenceModeError,
     'Inference mode `Other` is not supported.\nChoose `Local` or `Remote` instead.'),
    ('[global]\nstrategy = "test/strategy.toml"',
     'Local',
     ConfigSectionMissingError,
     'Missing `local` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false',
     'Local',
     ConfigSectionMissingError,
     'Missing `local.model` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\ndirectory = "models/"\nsuffix = ".gguf"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Local',
     ConfigParameterMissingError,
     'Missing `name` parameter in `local.model` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\nsuffix = ".gguf"',
     'Local',
     ConfigParameterMissingError,
     'Missing `directory` parameter in `local.model` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"',
     'Local',
     ConfigParameterMissingError,
     'Missing `suffix` parameter in `local.model` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"',
     'Remote',
     ConfigSectionMissingError,
     'Missing `remote` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\n[remote.service]\nurl = "http://localhost"\nport = 11434\nendpoint = "api/"',
     'Remote',
     ConfigParameterMissingError,
     'Missing `model` parameter in `remote` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\nmodel = "test-model-remote"',
     'Remote',
     ConfigSectionMissingError,
     'Missing `remote.service` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nport = 11434\nendpoint = "api/"',
     'Remote',
     ConfigParameterMissingError,
     'Missing `url` parameter in `remote.service` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nendpoint = "api/"',
     'Remote',
     ConfigParameterMissingError,
     'Missing `port` parameter in `remote.service` section in config file.'),
    ('[global]\nstrategy = "test/strategy.toml"\n[remote]\nmodel = "test-model-remote"\n[remote.service]\nurl = "http://localhost"\nport = 11434',
     'Remote',
     ConfigParameterMissingError,
     'Missing `endpoint` parameter in `remote.service` section in config file.'),
    ]
@pytest.mark.parametrize(['test_config','test_mode','error','message'],
                         test_method_load_raise_cases)
def test_method_load_raise(config,tmp_path,test_config,test_mode,error,message):
    # Build test config file
    test_path = tmp_path / 'test.toml'
    test_path.write_text(test_config)
    # Check exception raise
    with pytest.raises(error,match=message):
        config.load(test_mode)

test_method_load_warn_cases = [
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\ngpu = true\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Missing `format` parameter in `local` section, fallback to `None`.',
     ConfigData(model='test-model-local',strategy=Path('test/strategy.toml'),local=LocalConfigData(model=Path('models/test-model-local.gguf'),format=None,gpu=True,ram=False),remote=False)),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\nram = false\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Missing `gpu` parameter in `local` section, fallback to `False`.',
     ConfigData(model='test-model-local',strategy=Path('test/strategy.toml'),local=LocalConfigData(model=Path('models/test-model-local.gguf'),format='test-format',gpu=False,ram=False),remote=False)),
    ('[global]\nstrategy = "test/strategy.toml"\n[local]\nformat = "test-format"\ngpu = true\n[local.model]\nname = "test-model-local"\ndirectory = "models/"\nsuffix = ".gguf"',
     'Missing `ram` parameter in `local` section, fallback to `False`.',
     ConfigData(model='test-model-local',strategy=Path('test/strategy.toml'),local=LocalConfigData(model=Path('models/test-model-local.gguf'),format='test-format',gpu=True,ram=False),remote=False)),
    ]
@pytest.mark.parametrize(['test_config','message','ground_truth',],
                         test_method_load_warn_cases)
def test_method_load_warn(config,tmp_path,test_config,message,ground_truth):
    # Build test config file
    test_path = tmp_path / 'test.toml'
    test_path.write_text(test_config)
    # Check warning showing
    with pytest.warns(RuntimeWarning,match=message):
        result = config.load('Local')
    # Check load result
    assert result == ground_truth
    