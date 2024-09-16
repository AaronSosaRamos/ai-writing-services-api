from pydantic import BaseModel, Field
from typing import List, Dict, TypedDict, Optional

class AIWritingEnhancementInputSchema(BaseModel):
    text: str = Field(..., description="Text that needs enhancement.")
    lang: str = Field(..., description="Language of the text.")

class CorrectionSchema(BaseModel):
    before: str = Field(..., description="Original text.")
    after: str = Field(..., description="Corrected text.")
    explanation: str = Field(..., description="Explanation of the correction.")

class NormalizeTextCorrectionSchema(BaseModel):
    text: str = Field(..., description="The original text.")
    lang: str = Field(..., description="The language of the text.")
    corrected_normalize_text: str = Field(..., description="The corrected text after normalization.")
    normalize_corrections: List[CorrectionSchema] = Field(..., description="The list of corrections made during normalization.")

class AdvancedGrammarCorrectionSchema(BaseModel):
    normalized_text: str = Field(..., description="The original normalized text.")
    lang: str = Field(..., description="The language of the text.")
    corrected_advanced_grammar_text: str = Field(..., description="The corrected text after applying advanced grammar corrections.")
    advanced_grammar_corrections: List[CorrectionSchema] = Field(..., description="The list of corrections made for advanced grammar.")

class ClarityReadabilityTextCorrectionSchema(BaseModel):
    advanced_grammar_text: str = Field(..., description="The original text with advanced grammar.")
    lang: str = Field(..., description="The language of the text.")
    corrected_clarity_readability_text: str = Field(..., description="The corrected text after enhancing clarity and readability.")
    clarity_readability_corrections: List[CorrectionSchema] = Field(..., description="The list of corrections made to improve clarity and readability.")

class StylisticTextCorrectionSchema(BaseModel):
    clarity_readability_text: str = Field(..., description="The original text.")
    lang: str = Field(..., description="The language of the text.")
    corrected_style_text: str = Field(..., description="The corrected text after applying stylistic enhancements.")
    stylistic_corrections: List[CorrectionSchema] = Field(..., description="The list of corrections made during stylistic enhancement.")

class GraphState(TypedDict):
    text: str
    normalized_text: str
    advanced_grammar_text: str
    clarity_readability_text: str
    corrected_style_text: str
    lang: str
    normalize_corrections: List[CorrectionSchema]
    advanced_grammar_corrections: List[CorrectionSchema]
    clarity_readability_corrections: List[CorrectionSchema]
    stylistic_corrections: List[CorrectionSchema]