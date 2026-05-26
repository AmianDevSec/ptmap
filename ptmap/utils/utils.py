from urllib.parse import urlparse

def truncate_msg(msg: str, threshold: int = 10) -> str:
    index = len(msg) - threshold
    return f"{msg[:threshold]}...{msg[index:]}"

def is_url(value: str) -> bool:

    if not value: return
    
    try:

        parsed = urlparse(value)

        return all([
            parsed.scheme,
            parsed.netloc
        ])

    except Exception:
        return False
    
if __name__ == "__main__":
    print(is_url("https://target.com/page?x=fuzz"))
    print(is_url("target.txt"))
    