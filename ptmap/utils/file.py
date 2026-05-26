
from ptmap.utils.path import resolve_path

def load_file(file_name: str) -> list[str]:
    
    file_path = resolve_path(file_name)
    
    with open(file_path, "r", encoding="utf-8") as f:
        
        loaded_file_contents = [
            content.strip() for content in f.readlines()
        ]
    
    return loaded_file_contents