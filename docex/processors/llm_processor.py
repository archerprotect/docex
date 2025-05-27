import base64
import io
import json
import re
import logging
import traceback
from typing import List, Type, TypeVar, Optional, Dict, Any
from PIL import Image
from pydantic import BaseModel
import litellm
from .base_processor import BaseProcessor


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProcessor(BaseProcessor):
    """Processor that uses LiteLLM to access 100+ LLM models for document extraction."""

    def __init__(
        self,
        model: str = "gemini/gemini-1.5-flash",
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 32768,
        use_structured_output: bool = True,
        litellm_params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """
        Initialize the LLM processor with LiteLLM.

        Args:
            model: LiteLLM model string (e.g., "gpt-4-vision-preview", "claude-3-opus", "gemini/gemini-1.5-flash")
            api_key: API key for the model provider (can also be set via environment variables)
            api_base: Optional API base URL for custom endpoints
            system_prompt: Optional custom system prompt
            temperature: Model temperature for generation (default: 0.1)
            max_tokens: Maximum tokens to generate (default: 16384)
            use_structured_output: Whether to use function calling for structured output (default: True)
            litellm_params: Additional parameters to pass to litellm
            **kwargs: Additional keyword arguments passed to the model
        """
        self.model = model
        self.api_key = api_key
        self.api_base = api_base
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.use_structured_output = use_structured_output
        self.litellm_params = litellm_params or {}
        self.kwargs = kwargs

        if api_key:
            litellm.api_key = api_key
        if api_base:
            litellm.api_base = api_base

        self.system_prompt = system_prompt or self._get_default_system_prompt()

    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for document extraction."""
        return """You are an expert document extraction system. Your task is to analyze the provided document images and extract structured information according to the given schema.

Guidelines:
1. Carefully examine all pages of the document
2. Extract text, tables, and structured data accurately
3. Preserve the document's structure and formatting when relevant
4. Pay attention to layout, headings, lists, and tables
5. Extract data with high precision and completeness

Focus on accuracy and completeness. If certain fields cannot be found in the document, use null or empty values as appropriate."""

    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        return base64.b64encode(image_bytes).decode("utf-8")

    def _resolve_schema_refs(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve $ref references in Pydantic schema for Vertex AI compatibility."""
        if "$defs" not in schema:
            return schema

        defs = schema.pop("$defs")

        def _resolve(schema_part):
            # Remove default values that cause issues with Vertex AI
            if "default" in schema_part:
                del schema_part["default"]

            if "$ref" in schema_part:
                ref = schema_part.pop("$ref")
                ref_name = ref.split("/")[-1]
                if ref_name in defs:
                    schema_part.update(defs[ref_name])

            if "properties" in schema_part:
                for prop in schema_part["properties"].values():
                    _resolve(prop)

            if "items" in schema_part:
                _resolve(schema_part["items"])

            # Handle anyOf for Optional fields - convert to nullable
            if "anyOf" in schema_part:
                any_of = schema_part.pop("anyOf")
                # Find the non-null type
                for option in any_of:
                    if option.get("type") != "null":
                        schema_part.update(option)
                        schema_part["nullable"] = True
                        break

        _resolve(schema)
        return schema

    def _create_function_schema(self, schema: Type[T]) -> Dict[str, Any]:
        """Create a function schema for structured output from Pydantic model."""
        json_schema = schema.model_json_schema()

        # Resolve $ref and anyOf issues for Vertex AI compatibility
        resolved_schema = self._resolve_schema_refs(json_schema)

        return {
            "type": "function",
            "function": {
                "name": "extract_document_data",
                "description": "Extract structured data from the document according to the provided schema",
                "parameters": resolved_schema,
            },
        }

    async def process(self, images: List[Image.Image], schema: Type[T]) -> T:
        """
        Process document images using LiteLLM and extract data according to schema.

        Args:
            images: List of PIL Image objects (one per page)
            schema: Pydantic model class defining the expected output structure

        Returns:
            Instance of the schema populated with extracted data
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please analyze the following document pages and extract structured information. There are {len(images)} page(s) to process.",
                    }
                ],
            },
        ]

        for i, image in enumerate(images):
            base64_image = self._image_to_base64(image)
            messages[1]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                }
            )
            messages[1]["content"].append(
                {"type": "text", "text": f"Page {i + 1} of {len(images)}"}
            )

        call_params = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            **self.litellm_params,
            **self.kwargs,
        }

        if self.use_structured_output:
            try:
                function_schema = self._create_function_schema(schema)
                call_params["tools"] = [function_schema]
                call_params["tool_choice"] = {
                    "type": "function",
                    "function": {"name": "extract_document_data"},
                }

                response = await litellm.acompletion(**call_params)

                if response.choices[0].message.tool_calls:
                    function_call = response.choices[0].message.tool_calls[0]
                    if function_call.function.name == "extract_document_data":
                        json_data = json.loads(function_call.function.arguments)
                        return schema(**json_data)

                if response.choices[0].finish_reason == "length":
                    raise ValueError(
                        f"Model hit token limit. Increase max_tokens (current: {self.max_tokens})"
                    )
                
                raise ValueError("Model did not use function calling as expected")

            except Exception as e:
                logger.error(
                    f"Structured output failed, falling back to text parsing: {e}"
                )
                logger.error(traceback.format_exc())
                self.use_structured_output = False

        if not self.use_structured_output:
            schema_json = json.dumps(schema.model_json_schema(), indent=2)
            messages[1]["content"][0][
                "text"
            ] = f"""Please analyze the following document pages and extract information according to this schema:

```json
{schema_json}
```

Return only valid JSON that matches the schema exactly. No additional text or markdown formatting."""

            response = await litellm.acompletion(**call_params)

        if not response.choices[0].message.content:
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                raise ValueError(
                    f"Model hit token limit. Increase max_tokens (current: {self.max_tokens})"
                )
            else:
                raise ValueError(
                    f"Model returned no content. Finish reason: {finish_reason}"
                )

        response_text = response.choices[0].message.content

        try:
            json_data = json.loads(response_text)
        except json.JSONDecodeError:
            json_match = re.search(
                r"```(?:json)?\s*(.*?)\s*```", response_text, re.DOTALL
            )
            if json_match:
                json_data = json.loads(json_match.group(1))
            else:
                json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
                if json_match:
                    json_data = json.loads(json_match.group(0))
                else:
                    raise ValueError(
                        f"Could not extract valid JSON from response: {response_text}"
                    )

        return schema(**json_data)
