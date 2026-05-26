from rich.console import Console
from rich.theme import Theme
import datetime

custom_theme = Theme({

    # Informational / neutral
    "info": "cyan",

    # Successful actions
    "success": "green",

    # Warnings / suspicious states
    "warning": "yellow",

    # Errors / failures
    "error": "red",

    # Metadata / timestamps
    "time": "dim white",

})

console = Console(theme=custom_theme)

def format_message(message: str, prefix: str) -> str:
        """Add timestamp prefix to message."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        return f"[[time]{timestamp}[/time]] [[{prefix}]{prefix.upper()}[/{prefix}]] - {message}"

def logger(message: str, prefix: str = "info") -> None:
    """Log a message with a specified severity prefix.
    
    Args:
        message: The log message content to be displayed.
        prefix: The severity level of the log. Must be one of: 'info', 
            'error', or 'warning'.
    
    Returns:
        None
    
    Examples:
        >>> logger("User logged in", "info")
        >>> logger("Connection failed", "error")
        >>> logger("Disk space low", "warning")
    """
    
    formatted_message = format_message(prefix=prefix, message=message)
    console.print(formatted_message)


# logger("Bug FOUND", "info")
# Demonstrating all the styles
# console.print("This is information", style="info")
# console.print("[warning]The pod bay doors are locked[/warning]")
# console.print("Something terrible happened!", style="error")
