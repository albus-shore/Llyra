from pathlib import Path
import json

class Config:
    '''The class is defined to define basic attributes and internal methods, 
        for working with configurations.'''
    ### ============================ Dynamic Methods ============================ ###
    ## ========================== Initialize Method ========================== ##
    def __init__(self) -> None:
        '''The method is defined for initializing Config class object.'''
        # Define default path to config file
        self.config = 'config/config.json'
        # Define assistant internal attribute
        self._config: dict = None

    ## ======================== Internal Load Method ======================== ##
    def _load(self,path:str) -> dict:
        '''The method is defined for load config from default or custom path.
        Args:
            path: A string indicate the custom path to the config file.
        '''
        # Discriminate whether loading from custom path or default path
        if path:
            config_path:object = Path(path)
        else:
            config_path:object = Path(self.config)
        # Load config file
        try:
            config_json:str = config_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            if path:
                error = 'Error: Config file not found in provided path.'
            else:
                error = 'Error: Missing config file.'
            raise FileNotFoundError(error)
        else:
            self._config:dict = json.loads(config_json)
    
    ## ======================== Internal Write Method ======================== ##
    def _write(self,content:dict) -> None:
        '''The method id defined for write current config into file.
        Args:
            content: A dictionary indicate the current configurations.
        '''
        # Initialize new config file path
        path = Path(self.config)
        # Discriminate whether the file name has been occupied
        if path.exists():
            alarm = "Alarm: There is a existed config.json under '.config/'."
            alarm += "\n\t  This operation will rewrite all content in it."
            alarm += "\n\t  Send 'w' to confirm operation, "
            alarm += "Send 'q' to terminate process."
            while True:
                action = input(alarm)
                if action.lower() == 'w':
                    break
                elif action.lower() == 'q':
                    raise FileExistsError()
                else:
                    print('Invalid command.')
        # Transform content
        content = json.dumps(content)
        # Write file
        path.write_text(content,encoding='utf-8')
        # Terminal Information
        print("Current config has been write into '.config/config.json'.")

    ### ============================ Statics Methods ============================ ###
    ## ======================== Internal Path Method ======================== ##
    @staticmethod
    def path(path:str) -> str:
        '''The method is defined for struct of multi-kind path.
        Args:
            path: A string indicate the local path to a directory, 
                or base URL and endpoint path to a service.
        Returns:
            struct_path: A string indicate the valid path string 
                which ends with '/'.
        '''
        # Discriminate whether path end with '/'
        if path.endswith('/'):
            struct_path = path
        else:
            struct_path = path + '/'
        # Return struct path
        return struct_path