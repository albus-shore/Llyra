import time

## ========================== Record Function ========================== ##
def record(role:dict,input:str,output:str) -> dict:
    '''The function is defined for make single model inference record.
    Args:
        role: A dictionary indicate the role of input and output.
        input: A string indicate the query content.
        output: A string indicate the response content.
    Returns:
        record: A dictionary indicate the history of the object call.
    '''
    # Extract input and output role
    input_role = role['input']
    output_role = role['output']
    # Make record dictionary
    record = {
        "type": "call",
        "create_at": time.localtime(),
        input_role: input,
        output_role: output,
    }
    # Return record dictionary
    return record