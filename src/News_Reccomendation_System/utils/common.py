import os
from box.exceptions import BoxValueError  # if you don't want to create custom exeptions ,you can follow this
import yaml
from News_Reccomendation_System import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox   # See notes as to whywe used ConfigBox
from pathlib import Path
from typing import Any


@ensure_annotations
def read_yaml(path_to_file: Path) -> ConfigBox:
    '''
    Reads yaml file and returns ConfigBox
    
    Args:
        path_to_file (str): path like string input.
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file
        
    Returns:
        ConfigBox: ConfigBox type'''
    
    try:

        with open(path_to_file) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml file: {path_to_file} loaded succesfully')
            return ConfigBox(content)
        
    except BoxValueError:
        raise ValueError('yaml file is empty')
    
    except Exception as e:
        raise e
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose= True ):
    '''
    Creates directories from the list give as input
    
    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple directories is to be created
    
    '''

    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f'Created directory at : {path}')

        
@ensure_annotations
def save_json(path: Path, data: dict):
    '''
    Saves dictionary to json
    
    Args:
        path (Path): path to the json file
        data (dict): data to be saved in json file
    '''

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
    
    logger.info(f'Saved json file successfully at:{path}')


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    '''
    Loads json file in python
    
    Args:
        path (Path): path to json file
        
    Returns:
        ConfigBox: data as class attributes instead of dictionary
    '''
    with open(path) as f:
        content = json.load(f)
    
    logger.info(f"JSON file loaded succesfully from: {path}")

    return ConfigBox(content)


@ensure_annotations
def save_binary_file(data: Any, path: Path):
    '''
    Saves binary file
    
    Args:
        data (Any): data to be saved as binary
        path (Path): path to the binary file
    '''
    joblib.dump(value=data, filename=path)
    logger.info(f'Binary file saved at : {path}')



@ensure_annotations
def load_binary_file(path: Path) -> Any:
    '''
    Loads the data in a binary file
    
    Args:
        path (Path): path to the binary file
        
    Returns:
        Any: Object or data stored in the binary file
    '''
    data = joblib.load(path)
    logger.info(f'Binary file loaded from : {path}')
    
    return data



@ensure_annotations
def get_size(path: Path) -> str:
    '''
    Get the size of file in KB
    
    Args:
        path (Path): path to the file
    
    Returns:
        str: size in KB
    '''
    
    size_in_KB = round(os.path.getsize(path) / 1024)

    return f'----{size_in_KB} KB'