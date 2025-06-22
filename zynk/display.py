import time
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

def display_batch(batch, total_lines):
    used_lines = 0
    for article in batch:
        header = Table.grid(expand=True)
        header.add_column(ratio=3)                       # columna para el título
        header.add_column(justify="right",ratio=1)       # columna para la fecha
                
        title_text = f"[bold red][{article['source']}][/bold red]: {article['title']}"
        title = Text.from_markup(f"[link={article['link']}][bold]{title_text}[/bold][/link]")
        published = Text.from_markup(f"📅 [plum3]{article['published']}")
        
        header.add_row(title, published)

        
        summary = Text(article['summary'])
        body = Group(header, Text(), summary)

        panel = Panel(
            body,
            box=box.ROUNDED,
            padding=(1, 2),
            expand=False,
            border_style="orange1"
        )
        console.print(panel)

        used_lines += estimate_panel_height(article, console.size.width)

    remaining_lines = total_lines - used_lines - 1
    if remaining_lines > 0:
        console.print("\n" * remaining_lines, end="")

def wait_with_progress(seconds, width):
    with Progress(
        "⏳ [bold deep_sky_blue1][Remiaining Time]:" ,
        BarColumn(bar_width=width - 30), 
        TimeRemainingColumn(compact=True),
        "[bold plum3]secs",
        console=console,
        refresh_per_second=1
    ) as progress:
        task = progress.add_task("", total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.update(task, advance=1)

def estimate_panel_height(article, console_width):
    summary = Text(article["summary"])
    wrapped_lines = summary.wrap(console, width=console_width - 6)
    num_summary_lines = len(wrapped_lines)

    # Título con link + resumen + espaciado + padding + bordes
    return 2 + num_summary_lines + 1 + 2 + 2

