## ======================== Function `make_new_inference()` ======================== ##
def make_new_inference(role:str,content:str) -> dict:
    '''The function is defined for make single prompt record in chat iteration.
    Args:
        role: A string indicate the role of the content.
        content: A sting indicate the content of the prompt record.
    Returns:
        A dictionary indicate the single prompt record in chat iteration.
    '''
    # Make single prompt dictionary
    prompt = {'role':role,'content': content}
    # Return single prompt dictionary
    return prompt    