import shutil
from html.parser import HTMLParser

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

def get_terminal_rows():
    try:
        return shutil.get_terminal_size().lines
    except:
        return 30
