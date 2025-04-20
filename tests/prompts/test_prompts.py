import pytest
from llyra.local.prompts import Prompt

@pytest.fixture
def prompt():
    prompt = Prompt()
    return prompt

## ========================== Initialize Method Test ========================== ##
def test_class_initialize(prompt):
    '''Test whether the class can be initialized properly.'''
    assert prompt.begin == None
    assert prompt.end == None
    assert prompt.history == None
    assert prompt.rag == None
    assert prompt.tool == None
    assert prompt.iteration == ''

## =========================== Config Method Test =========================== ##
def test_config_method(prompt):
    '''Test whether the method can set prompt config parameters properly.'''
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    assert prompt.begin == '<|begin_of_sentence|>'
    assert prompt.end == '<|end_of_sentence|>'
    assert prompt.history == '<<|History|>>'
    assert prompt.rag == '<<|RAG|>>'
    assert prompt.tool == '<<|Tool|>>'
    assert prompt.iteration == ''

## ========================== Generate Methods Test ========================== ##
def test_call_method(prompt):
    '''Test whether the method can make prompt for single inference properly.'''
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': None,'rag': None,'tool':None})
    output = prompt.call({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!')
    assert output == '<|begin_of_sentence|><|User|>Evening!<|Assistant|><|end_of_sentence|>'
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': None,'rag': None,'tool':None})
    output = prompt.call({'input': '', 'output': '<|Assistant|>'},'Evening!')
    assert output == '<|begin_of_sentence|>Evening!<|Assistant|><|end_of_sentence|>'
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': None,'rag': None,'tool':None})
    output = prompt.call({'input': '', 'output': ''},'Evening!')
    assert output == 'Evening!'

def test_chat_method_without_iteration(prompt):
    # No prompt and iteration history
    '''Test whether the method can make prompt for iterative chat inference properly.'''
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    output = prompt.chat({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!',None)
    assert output == '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\n<|end_of_sentence|>'
    # Only with prompt
    system_prompt = 'You are a kind assistant.'
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    output = prompt.chat({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!',system_prompt)
    expectation = '<|begin_of_sentence|>\n\nYou are a kind assistant.\n<|end_of_sentence|>\n'
    expectation += '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\n<|end_of_sentence|>'
    assert output == expectation
    # Only with inference history
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    prompt.iterate('<|User|>','Evening!',False)
    prompt.iterate('<|Assistant|>','Evening!',True)
    output = prompt.chat({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!',None)
    expectation = '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\nEvening!\n<|end_of_sentence|>\n'
    expectation += '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\n<|end_of_sentence|>'
    assert output == expectation
    # With iteration history and prompt which has no placeholder
    system_prompt = 'You are a kind assistant.'
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    prompt.iterate('<|User|>','Evening!',False)
    prompt.iterate('<|Assistant|>','Evening!',True)
    output = prompt.chat({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!',system_prompt)
    expectation = '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\nEvening!\n'
    expectation += 'You are a kind assistant.\n<|end_of_sentence|>\n'
    expectation += '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\n<|end_of_sentence|>'
    assert output == expectation
    # With iteration history and prompt which has placeholder
    system_prompt = 'You are a kind assistant.\n<<|History|>>\nThere are history.'
    prompt.config({'begin':'<|begin_of_sentence|>','end':'<|end_of_sentence|>'},
                  {'history': '<<|History|>>','rag': '<<|RAG|>>','tool':'<<|Tool|>>'})
    prompt.iterate('<|User|>','Evening!',False)
    prompt.iterate('<|Assistant|>','Evening!',True)
    output = prompt.chat({'input': '<|User|>', 'output': '<|Assistant|>'},'Evening!',system_prompt)
    expectation = '<|begin_of_sentence|>\nYou are a kind assistant.\n'
    expectation += '<|User|>\nEvening!\n<|Assistant|>\nEvening!\n'
    expectation += 'There are history.\n<|end_of_sentence|>\n'
    expectation += '<|begin_of_sentence|>\n<|User|>\nEvening!\n<|Assistant|>\n<|end_of_sentence|>'
    assert output == expectation

## ========================== Additional Mtethods for Chat Test ========================== ##
def test_iterate_method(prompt):
    '''Test whether the method record iteration history properly.'''
    prompt.iterate('<|User|>','Evening!',False)
    assert prompt.iteration == '<|User|>\nEvening!'
    prompt.iterate(None,None,False)
    assert prompt.iteration == ''
    prompt.iterate('','Evening!',False)
    assert prompt.iteration == 'Evening!'
    prompt.iterate('<|User|>','',False)
    assert prompt.iteration == '<|User|>'
    prompt.iterate('<|User|>','Evening!',False)
    prompt.iterate('<|Assistant|>','Evening!',True)
    assert prompt.iteration == '<|User|>\nEvening!\n<|Assistant|>\nEvening!'
    prompt.iterate('<|User|>','Evening!',False)
    prompt.iterate('<|Assistant|>','Evening!',False)
    assert prompt.iteration == '<|Assistant|>\nEvening!'
