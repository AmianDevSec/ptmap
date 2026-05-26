from ptmap.utils.utils import is_url
import sys

def piped_input()-> list[str] | str:
    
    normalize_string = lambda x : [
        url for url in x.read().strip().splitlines()
        if is_url(url)
        ]
    
    normalized : list[None|str] = [None]
    
    if not sys.stdin.isatty():
        normalized = normalize_string(sys.stdin)
    
    return (
        normalized
        if all(normalized)
        else ''
    )