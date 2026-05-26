from pathlib import Path

def resolve_path(target: str) -> Path | None:

    if not target: return
    
    resolved = Path(
        target
    ).expanduser().resolve()

    return  (
        resolved
        if resolved.is_file()
        else None
    )