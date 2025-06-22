import argparse
import random
import shutil
import sys
from rich.console import Console
from pathlib import Path

from zynk.feeds import load_feeds_json, fetch_articles
from zynk.display import display_batch, wait_with_progress, estimate_panel_height
from zynk.utils import get_terminal_rows


default_path = Path(__file__).parent / "feed" / "default.json"
console = Console()

def main():
    parser = argparse.ArgumentParser(description="Terminal News Feed Viewer")
    parser.add_argument("-t", metavar= "time"     , dest = "time"         ,type=int, default=20             , help="Seconds to wait before refreshing (default: 20)")
    parser.add_argument("-f", metavar= "filename" , dest = "feedFilename" ,type=str, default=default_path   , help="Path to the feeds JSON file (default: feeds.json)")
    args = parser.parse_args()

    try:
        feeds = feeds = load_feeds_json(args.feedFilename)
    except FileNotFoundError as e:
        console.print(f"[red]{e}[/red]")
        sys.exit(1)


    articles = fetch_articles(feeds)
    if not articles:
        console.print("[red]No articles found. Check your internet or RSS feeds.[/red]")
        return

    shown = set()

    while True:
        rows = get_terminal_rows()
        columns = shutil.get_terminal_size().columns

        available = [a for a in articles if a["title"] not in shown]
        if len(available) < 1:
            shown.clear()
            available = articles.copy()

        # Seleccionar artículos que caben visualmente
        batch = []
        total_height = 0
        for a in random.sample(available, len(available)):
            est_height = estimate_panel_height(a, console_width=columns)
            if total_height + est_height <= rows - 1:
                batch.append(a)
                total_height += est_height
                shown.add(a["title"])
            if total_height >= rows - 1:
                break

        with console.screen():
            display_batch(batch, rows)
            try:
                wait_with_progress(args.time, width=columns)
            except KeyboardInterrupt:
                console.clear()
                console.print("Exiting. Have a great day! 🗞️")
                sys.exit(0)

if __name__ == "__main__":
    main()
