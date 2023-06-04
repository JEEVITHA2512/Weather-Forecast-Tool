import os
from platform import platform, system

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

# no tests for this function as it is not called anywhere in the command directly
def get_terminal_width() -> int:
    """
    Gets the width of the terminal.

    Returns:
        int: width of the terminal.
    """
    try:
        width, _ = os.get_terminal_size()
    except OSError:
        width = 80

    if system().lower() == "windows":
        width -= 1

    return width


def print_banner(console) -> None:
    """
    Prints the banner of the application.

    Args:
        console (Console): Rich console object.
    """

    banner = """

██╗    ██╗███████╗ █████╗ ████████╗██╗  ██╗███████╗██████╗  ██████╗██╗     ██╗
██║    ██║██╔════╝██╔══██╗╚══██╔══╝██║  ██║██╔════╝██╔══██╗██╔════╝██║     ██║
██║ █╗ ██║█████╗  ███████║   ██║   ███████║█████╗  ██████╔╝██║     ██║     ██║
██║███╗██║██╔══╝  ██╔══██║   ██║   ██╔══██║██╔══╝  ██╔══██╗██║     ██║     ██║
╚███╔███╔╝███████╗██║  ██║   ██║   ██║  ██║███████╗██║  ██║╚██████╗███████╗██║
 ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝
                                                                              

            """
    width = get_terminal_width()
    height = 10

    panel = Panel(
        Align(
            Text(banner, style="green"),
            vertical="middle",
            align="center",
        ),
        width=width,
        height=height,
        subtitle="[bold blue]v.1.0 by Atharva Shah for Microsoft Github Copilot Hackathon (TechGig)[/bold blue]",
    )
    console.print(panel)