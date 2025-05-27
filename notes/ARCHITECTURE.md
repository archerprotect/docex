# Docex Architecture

## 1. Overview

Docex is a Python library designed to provide a simple and extensible interface for Optical Character Recognition (OCR) and document understanding. It allows users to read various document types (PDFs, images, DOCX, etc.) and process their content using different backends, primarily Large Language Models (LLMs), to extract structured text in JSON format.

## 2. Project Structure

The project will be organized as follows:

```
docex/
├── __init__.py
├── loaders/                # Modules for reading different file types
│   ├── __init__.py
│   ├── base_loader.py      # Abstract base class for loaders
│   ├── pdf_loader.py
│   ├── image_loader.py
│   └── ...                 # Other loader implementations
├── processors/             # Modules for converting loaded content to text
│   ├── __init__.py
│   ├── base_processor.py   # Abstract base class for processors
│   ├── llm_processor.py    # Processor using LLMs (OpenAI, Gemini, etc.)
│   └── ...                 # Other processor implementations
├── models/                 # Data models and type definitions (Pydantic models)
│   ├── __init__.py
│   └── document.py         # Defines the structure of a processed document
├── core/                   # Core orchestration logic
│   ├── __init__.py
│   └── pipeline.py         # Manages the loading and processing workflow
├── utils/                  # Utility functions
│   ├── __init__.py
│   └── ...
tests/
├── ...                     # Unit and integration tests
examples/
├── ...                     # Usage examples
pyproject.toml
README.md
notes/
└── ARCHITECTURE.md
```

## 3. Core Components

The system is primarily composed of two types of pluggable components: Loaders and Processors.

### 3.1. Loaders

-   **Purpose**: Responsible for reading and parsing various input document formats.
-   **Location**: `docex/loaders/`
-   **Functionality**: Each loader will handle a specific file type (e.g., PDF, DOCX, PNG, JPG). It will take a file path or a file-like object as input and produce a standardized intermediate representation that can be consumed by Processors. This might involve extracting raw text, images, and basic layout information.
-   **Extensibility**: New loaders can be added by creating a new class that inherits from a `BaseLoader` abstract class and implements the required methods.

### 3.2. Processors

-   **Purpose**: Responsible for taking the output from a Loader and converting it into clean, structured Markdown text.
-   **Location**: `docex/processors/`
-   **Functionality**: These components will typically leverage LLMs (e.g., OpenAI GPT, Google Gemini, Anthropic Claude) or other OCR engines to interpret the content (including text, tables, images within the document) and generate Markdown. They might perform tasks like layout recognition, table extraction, and image captioning (if applicable).
-   **Extensibility**: New processors can be added by creating a new class that inherits from a `BaseProcessor` abstract class. This allows for integration with different LLM providers, local models, or traditional OCR tools.

### 3.3. Models

-   **Purpose**: Define the data structures used throughout the application, particularly for representing documents and their components.
-   **Location**: `docex/models/`

### 3.4. Core Pipeline

-   **Purpose**: Orchestrates the document processing workflow.
-   **Location**: `docex/core/pipeline.py`
-   **Functionality**:
    1.  Takes a document input (e.g., file path).
    2.  Selects the configured `Loader`, `Processor` and schema (a Pydantic model passed by the user)
    3.  Uses the `Loader` to parse the document into an intermediate representation.
    4.  Passes the intermediate representation to the `Processor` to generate the final model instance.
    5.  Handles errors and manages configurations for the process.

## 4. Extensibility and Pluggability

-   **Loaders**: As mentioned, new file formats can be supported by adding new loader classes inheriting from `BaseLoader`.
-   **Processors**: New processing backends (different LLMs, OCR engines, or custom logic) can be integrated by adding new processor classes inheriting from `BaseProcessor`.
-   **Schemas**: The schema (Pydantic model) passed by the user should be configurable.

