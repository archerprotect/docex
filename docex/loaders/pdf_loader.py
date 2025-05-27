from typing import List, Union, Optional
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_path
from .base_loader import BaseLoader


class PDFLoader(BaseLoader):
    """Loader for PDF documents."""
    
    def __init__(
        self, 
        dpi: int = 300,
        fmt: str = 'PNG',
        thread_count: int = 1,
        use_pdftocairo: bool = False,
        max_pages: Optional[int] = None
    ):
        """
        Initialize the PDF loader.
        
        Args:
            dpi: Resolution for rendering PDF pages to images (default: 300)
            fmt: Output image format (default: 'PNG')
            thread_count: Number of threads to use for conversion (default: 1)
            use_pdftocairo: Use pdftocairo instead of pdftoppm (default: False)
            max_pages: Maximum number of pages to process (default: None - process all)
        """
        self.dpi = dpi
        self.fmt = fmt
        self.thread_count = thread_count
        self.use_pdftocairo = use_pdftocairo
        self.max_pages = max_pages
    
    def load(self, source: Union[str, Path]) -> List[Image.Image]:
        """
        Load a PDF document and convert each page to an image.
        
        Args:
            source: Path to the PDF file
            
        Returns:
            List of PIL Image objects, one for each page
        """
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        if not self.supports_format(file_path):
            raise ValueError(f"File {file_path} is not a PDF")
        
        images = convert_from_path(
            str(file_path), 
            dpi=self.dpi,
            fmt=self.fmt,
            thread_count=self.thread_count,
            use_pdftocairo=self.use_pdftocairo
        )
        
        if self.max_pages and len(images) > self.max_pages:
            images = images[:self.max_pages]
            
        return images
    
    def supports_format(self, file_path: Union[str, Path]) -> bool:
        """
        Check if the file is a PDF.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file has a .pdf extension
        """
        file_path = Path(file_path)
        return file_path.suffix.lower() == '.pdf' 