import os
import json

class UtilJson():
    def __init__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise
    
    def __del__(self) -> None:
        try:
            pass
        except Exception as err:
            print(err)
            raise

    @classmethod
    def load_json(cls, filepath:str) -> dict:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data
    @classmethod
    def save_json(cls, data:dict, dirpath:str, filename:str) -> dict:
        if( os.path.exists(dirpath) is False):
            os.mkdir(dirpath)
        with open( os.path.join(dirpath, filename + '.json'), 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)