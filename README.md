# docex

Dead simple document extraction OCR powered by LLMs.

DocEx is a dead-simple, fully pluggable OCR toolkit designed to turn any document—PDFs, DOCX, images, scans—into clean, structured data using any of 100+ LLM models via LiteLLM.

## Features

- **100+ LLM Models**: Works with OpenAI, Anthropic, Google, Cohere, Replicate, Ollama, and many more via [LiteLLM](https://docs.litellm.ai/docs/providers)
- **Plug-and-Play**: Drop DocEx into your Python project via pip
- **Visual-First Processing**: Renders each page as an image, then leverages vision models to faithfully extract structured data
- **Schema-Based Extraction**: Define your data structure with Pydantic and let the LLM extract exactly what you need
- **Async & Sync APIs**: Use async/await or synchronous methods based on your needs
- **Extensible**: Easy to add new document loaders and processors
- **Simple Configuration**: Configure loaders and processors directly when instantiating them

## Installation

```bash
pip install docex-llm
```

Note: You'll also need to install poppler-utils for PDF processing:
- **macOS**: `brew install poppler`
- **Ubuntu/Debian**: `sudo apt-get install poppler-utils`
- **Windows**: Download from [poppler website](https://poppler.freedesktop.org/)

## Quick Start

```python
import asyncio
from pydantic import BaseModel
from docex import Pipeline, PDFLoader, LLMProcessor

# Define your extraction schema
class Invoice(BaseModel):
    invoice_number: str
    vendor_name: str
    total_amount: float
    items: list[dict]

# Use any LiteLLM-supported model
processor = LLMProcessor(
    model="gpt-4-vision-preview",  # or "claude-3-opus", "gemini/gemini-1.5-flash", etc.
    api_key="your-api-key",  # or set via environment variable
    temperature=0.1,
    max_tokens=4096
)

# Create pipeline with configured loader
pipeline = Pipeline(
    loader=PDFLoader(dpi=300, max_pages=10),
    processor=processor
)

# Process document
result = await pipeline.process_document(
    file_path="invoice.pdf",
    schema=Invoice
)

# Access extracted data
print(f"Invoice #{result.extracted_data.invoice_number}")
print(f"Total: ${result.extracted_data.total_amount}")
```

## Supported Models

DocEx supports any model available through LiteLLM, including:

- **OpenAI**: GPT-4 Vision, GPT-4, GPT-3.5
- **Anthropic**: Claude 3 Opus, Sonnet, Haiku
- **Google**: Gemini 1.5 Pro, Flash
- **Open Source**: Llama, Mistral, Mixtral via Ollama, Together, Replicate
- **And 100+ more**: See [LiteLLM docs](https://docs.litellm.ai/docs/providers) for full list

## Synchronous Usage

```python
# Use the synchronous wrapper
result = pipeline.process_document_sync(
    file_path="document.pdf",
    schema=YourSchema
)
```

## Loader Configuration

```python
# Configure PDF loader
loader = PDFLoader(
    dpi=300,  # Resolution for rendering
    fmt='PNG',  # Output format
    thread_count=4,  # Parallel processing
    max_pages=10  # Limit pages to process
)
```

## Processor Configuration

```python
# Configure LLM processor
processor = LLMProcessor(
    model="gpt-4-vision-preview",
    api_key="your-key",
    temperature=0.2,  # Control randomness
    max_tokens=8192,  # Max output length
    system_prompt="Custom instructions...",  # Override default prompt
    litellm_params={
        "timeout": 30,
        "max_retries": 2
    }
)
```

## Environment Variables

LiteLLM supports provider-specific environment variables:

```bash
# Provider API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
# etc.
```

## Advanced Usage

```python
# Custom system prompt for specialized extraction
processor = LLMProcessor(
    model="claude-3-opus-20240229",
    system_prompt="""You are a specialized invoice processor. 
    Focus on extracting line items with extreme precision.
    Always validate totals and tax calculations.""",
    temperature=0.0  # Deterministic output
)

# Process only first 5 pages of large documents
loader = PDFLoader(dpi=200, max_pages=5)

# Use with custom schema
class Contract(BaseModel):
    party_names: list[str]
    effective_date: str
    terms: list[dict]
    signatures: list[dict]

pipeline = Pipeline(loader=loader, processor=processor)
result = await pipeline.process_document("contract.pdf", Contract)
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
