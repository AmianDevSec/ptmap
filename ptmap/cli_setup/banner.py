import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def hero() -> None:
    """Display PTMAP banner"""

    ascii_banner = pyfiglet.figlet_format(
        "PTMAP",
        font="smslant"
    )

    content = f"""
[bold green]{ascii_banner.rstrip()}[/]

[dim]Path Traversal Fuzzer[/]

[bold green]>[/] [cyan]Repo[/]     [white]github.com/AmianDevSec/ptmap[/]
[bold green]>[/] [cyan]Support[/]  [white]ko-fi.com/amiandevsec[/]
"""

    console.print(
        Panel(
            Text.from_markup(content.rstrip()),
            padding=(0, 2),
            border_style="none"
        )
    )


if __name__ == "__main__":
    hero()