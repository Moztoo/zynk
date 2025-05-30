# Zynk

**Zynk** is a lightweight terminal-based RSS reader built in Python. It fetches and displays news from RSS feeds directly in your terminal, providing a fast and distraction-free reading experience.

> ⚠️ **Work in Progress**: This project is still under active development. Features and structure may change.

## Features

- Fetches and displays RSS feeds in the terminal.
- Simple JSON-based configuration (`feeds.json`).
- Fully written in Python — easy to extend or customize.

## Requirements

- Python 3.7+

## Installation

```bash
git clone https://github.com/Moztoo/zynk.git
cd zynk
```

(Optional) Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Edit `feeds.json` to include the RSS URLs you want to follow:

```json
{
  "feeds": [
    "https://example.com/rss",
    "https://another.com/rss"
  ]
}
```

2. Run the script:

```bash
python zynk.py
```

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch for your changes
3. Submit a pull request

## License

MIT License — see [`LICENSE`](LICENSE) file for details.
