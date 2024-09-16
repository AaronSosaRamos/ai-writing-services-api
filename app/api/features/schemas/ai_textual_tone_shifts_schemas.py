from pydantic import BaseModel, Field
from typing import List, TypedDict

class AITextualToneShiftInputSchema(BaseModel):
    text: str = Field(..., description="Text that needs connectors.")
    lang: str = Field(..., description="Language of the text.")
    target_tone: str = Field(..., description="The required tone for the text")

class ToneAnalysisSchema(BaseModel):
    sentence: str = Field(..., description="The sentence or segment being analyzed for tone.")
    current_tone: str = Field(..., description="The identified tone of the sentence (e.g., formal, informal, emotional, technical).")
    change_needed: bool = Field(..., description="Whether a tone shift is necessary for this segment.")
    reason: str = Field(..., description="Explanation of why the tone shift is needed, if applicable.")

class ToneShiftSuggestionSchema(BaseModel):
    sentence: str = Field(..., description="The sentence or segment for which the tone shift is being suggested.")
    suggested_tone: str = Field(..., description="The target tone that should replace the current tone (e.g., formal, persuasive, technical).")
    suggestion: str = Field(..., description="The specific changes suggested to shift the tone, including word choices, sentence structures, etc.")
    position: int = Field(..., description="The position in the text where the tone shift suggestion applies.")

class ToneShiftImplementationSchema(BaseModel):
    original_sentence: str = Field(..., description="The original sentence before the tone shift was applied.")
    revised_sentence: str = Field(..., description="The sentence after the tone shift was applied.")
    final_review: str = Field(..., description="Evaluation of whether the tone shift was successful (yes/no).")
    review_notes: str = Field(..., description="Any notes or feedback on the success of the tone shift.")

class ToneAnalysisResponseSchema(BaseModel):
  tone_analysis: List[ToneAnalysisSchema] = Field(..., description="The tone analysis of the text")

class ToneShiftSuggestionSchema(BaseModel):
  tone_shift_suggestions: List[ToneShiftSuggestionSchema] = Field(..., description="The list of tone shift suggestions of the text")

class ToneShiftImplementationResponseSchema(BaseModel):
  tone_shift_implementation: List[ToneShiftImplementationSchema] = Field(..., description="The list of tone shift implementations of the text")
  final_text: str = Field(..., description="The final text of the text")
  final_review: str = Field(..., description="The final review of the text")
  review_notes: str = Field(..., description="The final review notes of the text")

class FinalCheckResponseSchema(BaseModel):
  final_check: str = Field(..., description="The final check to evaluate if the text passes all the criteria about tone shifting. You must only answer 'yes' or 'no' in lower case")

class GraphState(TypedDict):
    text: str
    lang: str
    target_tone: str

    tone_analysis: List[ToneAnalysisSchema]

    tone_shift_suggestions: List[ToneShiftSuggestionSchema]

    tone_shift_implementation: List[ToneShiftImplementationSchema]

    final_text: str
    final_review: str
    review_notes: str

    final_check: str