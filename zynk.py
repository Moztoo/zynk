import feedparser
import random
import time
import shutil
import webbrowser
import sys
import argparse
import json
from pathlib import Path
import requests
from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TimeRemainingColumn, track
from rich.text import Text
from rich.table import Table
from rich import box
from html.parser import HTMLParser

console = Console()
articles = []

def load_feeds_json(path="feeds.json"):
    file = Path(path)
    if not file.exists():
        console.print(f"[red]Feed file '{path}' not found![/red]")
        sys.exit(1)
    with file.open("r", encoding="utf-8") as f:
        return json.load(f)

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data)
    def get_data(self):
        return ''.join(self.text)

def strip_html(html):
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_data()

def extract_content(entry, max_chars=400):
    if "content" in entry and entry.content:
        raw = entry.content[0].value
    else:
        raw = entry.get("summary", "")
    clean = strip_html(raw)
    return "-> " + clean[:max_chars].strip()

def load_articles(feeds, timeout=5):
    global articles
    articles = []

    console.print(f"[cyan]📡 Fetching news feeds (timeout: {timeout}s)...[/cyan]\n")
    for source_name, url in track(feeds.items(), description="Loading feeds...", total=len(feeds)):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            for entry in feed.entries:
                articles.append({
                    "title": entry.title,
                    "summary": extract_content(entry),
                    "link": entry.link,
                    "source": source_name
                })
        except (requests.exceptions.RequestException, Exception) as e:
            console.print(f"[yellow]⚠️ Skipping {source_name}: {e}[/yellow]")

def display_batch(batch, total_lines):
    used_lines = 0
    for article in batch:
        title = Text(article['title'], style="bold")
        summary = Text(article['summary'])

        footer = Table.grid(expand=True)
        footer.add_column(ratio=1)
        footer.add_column(justify="right", no_wrap=True)
        footer.add_row("", f"[link={article['link']}]link[/link]")

        body = Group(title, Text(), summary, Text(), footer)

        panel = Panel(
            body,
            title=f"📰 {article['source']}",
            box=box.ROUNDED,
            padding=(1, 2),
            expand=True
        )
        console.print(panel)
        used_lines += 12

    remaining_lines = total_lines - used_lines - 1
    if remaining_lines > 0:
        console.print("\n" * remaining_lines, end="")

def wait_with_progress(seconds, width):
    with Progress(
        BarColumn(bar_width=width - 30),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console,
        transient=False,
        refresh_per_second=1
    ) as progress:
        task = progress.add_task("", total=seconds)
        for _ in range(seconds):
            time.sleep(1)
            progress.update(task, advance=1)

def get_terminal_rows():
    try:
        return shutil.get_terminal_size().lines
    except:
        return 30

def main():
    parser = argparse.ArgumentParser(description="Terminal News Feed Viewer")
    parser.add_argument("-t", type=int, default=20, help="Seconds to wait before refreshing (default: 20)")
    args = parser.parse_args()

    feeds = load_feeds_json()
    load_articles(feeds)
    if not articles:
        console.print("[red]No articles found. Check your internet or RSS feeds.[/red]")
        return

    shown = set()
    card_height = 10

    while True:
        rows = get_terminal_rows()
        columns = shutil.get_terminal_size().columns
        cards_per_screen = max(1, (rows - 1) // card_height)

        available = [a for a in articles if a["title"] not in shown]
        if len(available) < cards_per_screen:
            shown.clear()
            available = articles.copy()

        batch = random.sample(available, cards_per_screen)
        for a in batch:
            shown.add(a["title"])

        with console.screen():
            display_batch(batch, rows)
            try:
                wait_with_progress(args.t, width=columns)
            except KeyboardInterrupt:
                console.clear()
                console.print("Exiting. Have a great day! 🗞️")
                sys.exit(0)

if __name__ == "__main__":
    main()
