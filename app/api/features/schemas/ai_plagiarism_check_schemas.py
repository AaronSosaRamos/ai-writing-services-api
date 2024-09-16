from pydantic import BaseModel, Field
from typing import List, TypedDict

class AIPlagiarismCheckInputSchema(BaseModel):
    original_text: str = Field(..., description="The original text.")
    comparison_text: str = Field(..., description="The text that will be compared to find plagiarism.")
    lang: str = Field(..., description="The language of the texts")

class TextAnalysisSchema(BaseModel):
    sentence_original: str = Field(..., description="The sentence from the original text being analyzed for plagiarism.")
    sentence_comparison: str = Field(..., description="The sentence from the comparison text being compared for plagiarism.")
    likelihood_of_plagiarism: float = Field(..., description="The likelihood that this sentence is plagiarized, between 0 and 1.")
    flagged_for_review: bool = Field(..., description="Whether this sentence should be flagged for review due to suspicious similarities.")

class PlagiarismSuspicionSuggestionSchema(BaseModel):
    sentence_original: str = Field(..., description="The sentence from the original text flagged as potentially plagiarized.")
    sentence_comparison: str = Field(..., description="The sentence from the comparison text that is similar to the flagged sentence.")
    suggestion: str = Field(..., description="A suggestion on why this sentence may be plagiarized, including detected patterns or similarities.")
    likelihood_of_plagiarism: float = Field(..., description="The likelihood that this part of the text is plagiarized, based on detected patterns.")

class PlagiarismCorrectionSchema(BaseModel):
    original_sentence: str = Field(..., description="The original sentence flagged as plagiarized.")
    corrected_sentence: str = Field(..., description="The revised sentence to avoid suspicion of plagiarism.")
    reason_for_correction: str = Field(..., description="Explanation for why this sentence was corrected, based on detected patterns.")

class FinalPlagiarismCheckSchema(BaseModel):
    final_text: str = Field(..., description="The final version of the text after corrections have been applied.")
    final_check: str = Field(..., description="The final determination of whether the text is likely plagiarized. Answer must be 'yes' or 'no' in lowercase.")
    review_notes: str = Field(..., description="Additional notes or comments on the final evaluation of the text.")

class IsPlagiarismResponseSchema(BaseModel):
    is_plagiarized: str = Field(..., description="Whether the text is likely plagiarized. Answer must be 'yes' or 'no' in lowercase.")
    plagiarism_level: int = Field(..., description="The plagiarism percentage. It must be from 0 to 100 (Integer).")

class TextAnalysisResponseSchema(BaseModel):
    text_analysis: List[TextAnalysisSchema] = Field(
        ..., description="The detailed analysis of the text, indicating the likelihood of plagiarism between two texts for each sentence."
    )

class PlagiarismSuspicionSuggestionResponseSchema(BaseModel):
    plagiarism_suspicion_suggestions: List[PlagiarismSuspicionSuggestionSchema] = Field(
        ..., description="List of sentences flagged as potentially plagiarized, with suggestions on why they may be considered plagiarized."
    )

class PlagiarismCorrectionResponseSchema(BaseModel):
    plagiarism_corrections: List[PlagiarismCorrectionSchema] = Field(
        ..., description="List of corrections applied to sentences or segments that were flagged as plagiarized to reduce suspicion."
    )

class FinalPlagiarismCheckResponseSchema(BaseModel):
    final_plagiarism_check: FinalPlagiarismCheckSchema = Field(
        ..., description="The final evaluation determining if the text passes the plagiarism check between the two texts, with a 'yes' or 'no' answer and review notes."
    )

class GraphState(TypedDict):
    original_text: str
    comparison_text: str
    lang: str

    is_plagiarized: str
    plagiarism_level: int

    text_analysis: List[TextAnalysisSchema]

    plagiarism_suspicion_suggestions: List[PlagiarismSuspicionSuggestionSchema]

    plagiarism_corrections: List[PlagiarismCorrectionSchema]

    final_plagiarism_check: FinalPlagiarismCheckSchema