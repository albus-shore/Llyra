import pytest
from llyra.components.configs.utils.funcs import struct_model_name, struct_path, \
    struct_suffix, struct_url

## ========================== Test `struct_path` function ========================== ##
def test_function_struct_path_with_formatted_path():
    assert 'test_path/' == struct_path('test_path/')

def test_function_struct_path_with_unformatted_path():
    assert 'test_path/' == struct_path('test_path')

## ========================= Test `struct_suffix` function ========================= ##
def test_function_struct_suffix_with_formatted_suffix():
    assert '.test' == struct_suffix('.test')

def test_function_struct_suffix_with_unformatted_suffix():
    assert '.test' == struct_suffix('test')

## ======================= Test `struct_model_name` function ======================= ##
def test_function_struct_model_name_with_formatted_model_name():
    assert 'test_model' == struct_model_name('test_model')

def test_function_struct_model_name_with_unformatted_model_name():
    assert 'test_model' == struct_model_name('test_model.gguf')

## ========================== Test `struct_url` function ========================== ##
def test_function_struct_url_with_formatted_url():
    assert '127.0.0.1' == struct_url('127.0.0.1')

def test_function_struct_url_with_unformatted_url():
    assert '127.0.0.1' == struct_url('127.0.0.1/')