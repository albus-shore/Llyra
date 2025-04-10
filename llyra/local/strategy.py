from pathlib import Path
import json

## ========================== Strategy Load Function ========================== ##
def load(path:str):
    '''The funcrion is defind for load infer strategy file.
    Args:
        path: A string indicate the path to the strategy file.
        input_role: A string indicate the role of input.
        output_role: A string indicate the role of output.
        stop: A string indicate where the model should stop generation.
    Returns:
        strategy:
            role, stop\n
            role: A dictionary indicate the role of input and output.\n
            stop: A string indicate where the model should stop generation.\n
            max_token: A int indicate the model's max token number of inference.
    '''
    # Load strategy file
    strategy_path:object = Path(path)
    try:
        strategy_json = strategy_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        raise FileNotFoundError('Error: Missing strategy file.')
    else:
        strategy_dictionary:dict = json.loads(strategy_json)
        # Read strategy parameters
        try:
            role = strategy_dictionary['role']
            stop = strategy_dictionary['stop']
            max_token = strategy_dictionary['max_token']
            max_token = int(max_token)
        except IndexError:
            raise IndexError('Error: Missing necessary keys.')
        else:
            return role,stop,max_token