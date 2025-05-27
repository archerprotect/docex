from abc import ABC, abstractmethod
from typing import List, Type, TypeVar
from PIL import Image
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseProcessor(ABC):
    """Abstract base class for document processors."""
    
    @abstractmethod
    async def process(self, images: List[Image.Image], schema: Type[T]) -> T:
        """
        Process a list of images and extract structured data according to the schema.
        
        Args:
            images: List of PIL Image objects (one per page)
            schema: Pydantic model class defining the expected output structure
            
        Returns:
            Instance of the schema populated with extracted data
        """
        pass 