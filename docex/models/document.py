from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Metadata about a processed document."""

    file_path: str
    page_count: int
    processing_time: float = Field(description="Processing time in seconds")
    processor_used: str
    model_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ProcessedDocument(BaseModel):
    """Container for a processed document with metadata."""

    metadata: DocumentMetadata
    extracted_data: Any
