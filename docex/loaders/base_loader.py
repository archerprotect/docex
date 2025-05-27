from abc import ABC, abstractmethod
from typing import List, Union, Any
from pathlib import Path
from PIL import Image


class BaseLoader(ABC):
    """Abstract base class for document loaders."""
    
    @abstractmethod
    def load(self, source: Union[str, Path]) -> List[Image.Image]:
        """
        Load a document and return a list of images (one per page).
        
        Args:
            source: Path to the document file
            
        Returns:
            List of PIL Image objects, one for each page
        """
        pass
    
    @abstractmethod
    def supports_format(self, file_path: Union[str, Path]) -> bool:
        """
        Check if this loader supports the given file format.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the loader can handle this file format
        """
        pass 