import asyncio
import time
from pathlib import Path
from typing import Type, TypeVar, Union, Optional
from pydantic import BaseModel

from ..loaders import BaseLoader, PDFLoader
from ..processors import BaseProcessor
from ..models import DocumentMetadata, ProcessedDocument

T = TypeVar("T", bound=BaseModel)


class Pipeline:
    """Main pipeline for document processing."""

    def __init__(
        self,
        loader: Optional[BaseLoader] = None,
        processor: Optional[BaseProcessor] = None,
    ):
        """
        Initialize the pipeline with loader and processor.

        Args:
            loader: Document loader instance (defaults to PDFLoader)
            processor: Document processor instance (must be provided)
        """
        self.loader = loader or PDFLoader()
        self.processor = processor

        if not self.processor:
            raise ValueError("A processor must be provided to the pipeline")

    async def process_document(
        self,
        file_path: Union[str, Path],
        schema: Type[T],
    ) -> ProcessedDocument:
        """
        Process a document and extract structured data.

        Args:
            file_path: Path to the document file
            schema: Pydantic model class defining the expected output structure

        Returns:
            ProcessedDocument containing metadata and extracted data
        """
        file_path = Path(file_path)

        start_time = time.time()

        images = self.loader.load(file_path)

        extracted_data = await self.processor.process(images, schema)

        processing_time = time.time() - start_time

        metadata = DocumentMetadata(
            file_path=str(file_path),
            page_count=len(images),
            processing_time=processing_time,
            processor_used=self.processor.__class__.__name__,
            model_name=getattr(self.processor, "model", None),
        )

        result = ProcessedDocument(
            metadata=metadata,
            extracted_data=extracted_data,
        )

        return result

    def process_document_sync(
        self,
        file_path: Union[str, Path],
        schema: Type[T],
    ) -> ProcessedDocument:
        """
        Synchronous wrapper for process_document.

        Args:
            file_path: Path to the document file
            schema: Pydantic model class defining the expected output structure

        Returns:
            ProcessedDocument containing metadata and extracted data
        """
        return asyncio.run(self.process_document(file_path, schema))
