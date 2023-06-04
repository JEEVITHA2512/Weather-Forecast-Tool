import time

from rich import box, print
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import track
from rich.syntax import Syntax


def print_about_app() -> None:
    """
    Prints the about app page

    1. Create a layout object
    2. Create a header content object with the help of the Panel class
    3. Create a footer content object with the help of the Panel class
    4. Create a main content object with the help of the Panel class
    5. Divide the "screen" into three parts
    6. Update the header, main and footer with their respective content objects
    7. Print the layout which contains details about the app
    """
    layout = Layout()

    header_content = Panel(
        renderable="📚 [gold1 bold]WeatherCLI[/gold1 bold] is a lightweight [i u]Command Line Interface[/i u] that retrieves the current weather forecast for a city by leveraging the OpenWeatherMap API. Built with Python and GitHub Copilot, showcasing seamless API usage, data parsing, and error handling. With the power of [bold green]rich[/bold green] and [bold green]typer[/bold green]. as command line building packages.",
        title="[reverse]ABOUT WEATHER CLI[/reverse]",
        title_align="center",
        border_style="bold green",
        padding=(1, 1),
        box=box.DOUBLE_EDGE,
        highlight=True,
    )

    # Divide the "screen" in to three parts
    layout.split()
    