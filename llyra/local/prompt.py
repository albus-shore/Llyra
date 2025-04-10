## ========================== Prompt Function ========================== ##
def prompt(role:dict,message:str) -> str:
    '''The function is defined for make prompt for model inference.
    Args:
        role: A dictionary indicate the input role and output role
        message: A message indicate the input content.
    Returns:
        prompt: A string indicate the prompt for model inference.
    '''
    # Extract input and output role
    input_role = role['input']
    output_role = role['output']
    # Make prompt content
    prompt = input_role + message + output_role
    # Return prompt content
    return prompt