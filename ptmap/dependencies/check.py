def is_vulnerable(status: int, body: str) -> bool:
    flags = ["root:", "daemon:", "[fonts]", "[extensions]"]
    check_flags = [
        True if flag in body 
        else False 
        for flag in flags
        ]
    
    verdict = status == 200 and any(check_flags)
    return verdict
