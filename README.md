# docex

Dead simple document extraction OCR powered by LLMs.

DocEx is a dead-simple, fully pluggable OCR toolkit designed to turn any document—PDFs, DOCX, images, scans—into clean, structured Markdown for seamless AI ingestion.

## Features

- **Plug-and-Play**: Drop DocEx into your Node.js or Python project via npm or pip.
- **Universal Input**: Accepts PDFs (via Poppler/GraphicsMagick), images (JPEG, PNG, TIFF), and more.
- **Visual-First Processing**: Renders each page as an image, then leverages vision + LLMs to faithfully transcribe layouts, tables, charts, and free-form text.
- **Markdown Output**: Aggregates per-page results into a single Markdown document, preserving headings, lists, code blocks, tables, and inline images.
- **Extensible Backends**: Works out-of-the-box with OpenAI, Azure OpenAI, AWS Bedrock, Google Gemini, Vertex AI (Python only), plus any model with an HTTP API.
- **Customizable Prompts & Workflows**: Configure system prompts, error handling modes, concurrency, page selection, orientation correction, and more.

In short, docEx converts the visual complexity of your documents into developer-friendly Markdown—no heavy tuning, no brittle heuristics, just plug in and extract.

## Installation

```bash
pip install docex
```

## Usage

```python
# Example usage to be added here
```

## Development

This project uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

1. Install Poetry: `pip install poetry`
2. Clone the repository: `git clone https://github.com/yourusername/docex.git`
3. Navigate to the project directory: `cd docex`
4. Install dependencies: `poetry install`

### Running Tests

```bash
poetry run poe test
```

### Linting

```bash
poetry run poe lint
```
