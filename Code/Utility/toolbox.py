# import git
import ast 
import os

from datetime import datetime
from functools import wraps
import time


## printing stuff
def printline():
    print("---" * 50)

def find_repo_root(startpath=os.getcwd()):
    current_path = os.path.abspath(startpath) # Path started on
    while True:
        if os.path.isdir(os.path.join(current_path, '.git')) or os.path.isfile(os.path.join(current_path, 'README.md')): # If on git path, return it
            ret = current_path
            break
        
        parent_path = os.path.dirname(current_path)

        if parent_path == current_path: # If current path is parent path, stop 
            break
        current_path = parent_path # Set current path to parent path, to check if git path again
    if ret:
        return ret.replace("\\", "/")
    else:
        return None


## data structure management (for dicts inside of dataframes, etc)
def eval_pd_data_string_literal(x):
    """
    Evaluate a data string within a pandas frame literally (as dict, list, etc).
    Note, def not perfect
    """
    try:
        return ast.literal_eval(x)
    except Exception:
        # If parsing fails, check if the string is in the format "a,b,c"
        if isinstance(x, str) and ',' in x: 
            return [item.strip() for item in x.split(',')]
        return None

## time management
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        printline()
        print(f"Started {func.__name__} at {get_current_time()}")
        result = func(*args, **kwargs)
        end_time = time.time()  # Record end time
        elapsed_time = end_time - start_time  # Calculate elapsed time
        print(f"Finished {func.__name__} at {get_current_time()}")
        print(f"Total time elapsed: {elapsed_time:.4f} seconds")  # Print elapsed time
        printline()
        print("\n")
        return result
    return wrapper

## accessing stuff we want a lot
def get_genres():
    with open(f"{find_repo_root()}/Data/general/genre_list.txt", "r") as f:
        return f.read().splitlines() 

