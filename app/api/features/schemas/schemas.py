from typing import Optional, List
from pydantic import BaseModel, Field, validator

class RequestSchema(BaseModel):
    lang: str = Field(..., min_length=2, max_length=2, pattern='^[a-zA-Z]{2}$', description="Language code for the presentation")
    content: str = Field(..., min_length=1, description="The content for the spelling checking process")

    @validator('lang')
    def validate_language(cls, v):
        if v.lower() not in ['en', 'es', 'fr', 'de', 'it', 'pt']:
            raise ValueError('Invalid language code')
        return v
    
class SpellingCheckerRequestArgs:
    def __init__(self, spelling_checker_schema: RequestSchema):
        self._spelling_checker_schema = spelling_checker_schema

    @property
    def content(self) -> str:
        return self._spelling_checker_schema.content

    @content.setter
    def content(self, value: str):
        self._spelling_checker_schema.content = value

    @property
    def lang(self) -> str:
        return self._spelling_checker_schema.lang

    @lang.setter
    def lang(self, value: str):
        self._spelling_checker_schema.lang = value

    def validate_and_return(self) -> dict:
        # Validate the SlideSchema and return the values as a dictionary
        return self._spelling_checker_schema.dict()

class Suggestion(BaseModel):
    originalWord: str
    suggestedWords: List[str]
    context: Optional[str] = Field(None, description="Context in which the word is found for better accuracy")

class ErrorDetail(BaseModel):
    position: int = Field(..., description="Position of the error in the original text")
    length: int = Field(..., description="Length of the word with the error")
    message: str = Field(..., description="Message describing the type of error")
    severity: str = Field(..., description="Severity of the error (e.g., 'low', 'medium', 'high')")

class SpellingCheckerResult(BaseModel):
    result: str = Field(..., description="The text after the spelling check")
    hasAnyError: bool = Field(..., description="Indicates whether any errors were found during the spelling check")
    errorExplanation: Optional[str] = Field(None, description="General explanation of the errors found")
    suggestions: Optional[List[Suggestion]] = Field(None, description="List of correction suggestions with details")
    errors: Optional[List[ErrorDetail]] = Field(None, description="List of detailed information about the errors found")
    language: str = Field(..., description="Language in which the spelling check was performed")
    processingTime: float = Field(..., description="Time in seconds it took to process the text")
    confidenceScore: Optional[float] = Field(None, description="Confidence score indicating the accuracy of the check (0-1)")