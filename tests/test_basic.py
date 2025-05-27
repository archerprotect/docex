import pytest
from pydantic import BaseModel

from docex.loaders import PDFLoader
from docex.processors import LLMProcessor
from docex.core import Pipeline


class TestPDFLoader:
    """Test the PDF loader functionality."""

    def test_supports_format(self):
        loader = PDFLoader()
        assert loader.supports_format("test.pdf") == True
        assert loader.supports_format("test.PDF") == True
        assert loader.supports_format("test.jpg") == False
        assert loader.supports_format("test.docx") == False

    def test_loader_initialization(self):
        loader = PDFLoader(dpi=150)
        assert loader.dpi == 150


class TestPipeline:
    """Test the pipeline functionality."""

    def test_pipeline_requires_processor(self):
        with pytest.raises(ValueError, match="A processor must be provided"):
            Pipeline(loader=PDFLoader(), processor=None)


class TestLLMProcessor:
    """Test the LLM processor functionality."""

    def test_processor_initialization(self):
        processor = LLMProcessor(model="gpt-4-vision-preview", api_key="test-key")
        assert processor.model == "gpt-4-vision-preview"
        assert processor.api_key == "test-key"

    def test_processor_with_litellm_params(self):
        processor = LLMProcessor(
            model="claude-3-opus-20240229", litellm_params={"timeout": 30}
        )
        assert processor.litellm_params["timeout"] == 30


class SimpleSchema(BaseModel):
    """Simple test schema."""

    text: str
    page_count: int
