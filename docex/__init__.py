"""
Docex - Dead simple document extraction OCR powered by LLMs.
"""

from .core import Pipeline
from .loaders import PDFLoader
from .processors import LLMProcessor
from .models import DocumentMetadata, ProcessedDocument

__version__ = "0.1.0"

__all__ = [
    "Pipeline",
    "PDFLoader", 
    "LLMProcessor",
    "DocumentMetadata",
    "ProcessedDocument"
]

