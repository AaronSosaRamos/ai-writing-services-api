from typing import List, TypedDict
from pydantic import BaseModel
from pydantic import Field

class AIAdditionOfConnectorsInputSchema(BaseModel):
    text: str = Field(..., description="Text that needs connectors.")
    lang: str = Field(..., description="Language of the text.")

class CorrectionSchema(BaseModel):
    start_index: int = Field(..., description="The starting index of the text where the correction begins.")
    end_index: int = Field(..., description="The ending index of the text where the correction ends.")
    correction: str = Field(..., description="The suggested correction for the specified text segment.")
    explanation: str = Field(..., description="Explanation of why the correction is necessary.")

class LogicalRelationSchema(BaseModel):
    sentence: str = Field(..., description="The sentence being analyzed for logical relationships.")
    relation: str = Field(..., description="The type of logical relationship identified (e.g., cause-effect, contrast).")
    confidence: float = Field(..., description="The confidence score of the identified relationship, between 0 and 1.")

class ConnectorSuggestionSchema(BaseModel):
    connector: str = Field(..., description="The suggested logical connector to enhance the coherence of the text.")
    position: int = Field(..., description="The position in the text where the connector should be inserted.")
    relation_type: str = Field(..., description="The type of logical relationship that the connector is addressing.")

class LogicalRelationsResponseSchema(BaseModel):
  logical_relations: List[LogicalRelationSchema] = Field(..., description="The suggested logical relations for the connectors in the text")

class ConnectorSuggestionResponseSchema(BaseModel):
  connector_suggestions: List[ConnectorSuggestionSchema] = Field(..., description="The suggested connectors for the text")

class TextWithConnectorsResponseSchema(BaseModel):
  text_with_connectors: str = Field(..., description="The text with the suggested connectors")

class FluencyCorrectionsResponseSchema(BaseModel):
  fluency_corrections: List[CorrectionSchema] = Field(..., description="The suggested fluency corrections for the text")

class FinalTextResponseSchema(BaseModel):
  final_text: str = Field(..., description="The final text")

class FinalCheckResponseSchema(BaseModel):
  final_check: str = Field(..., description="The final check to evaluate if the text passes all the criteria about connectors. You must only answer 'yes' or 'no' in lower case"),

class GraphState(TypedDict):
    text: str
    lang: str

    logical_relations: List[LogicalRelationSchema]
    connector_suggestions: List[ConnectorSuggestionSchema]

    text_with_connectors: str

    fluency_corrections: List[CorrectionSchema]
    final_check: str
    final_text: str